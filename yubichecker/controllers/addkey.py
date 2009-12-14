import logging

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from yubichecker.model import *

from yubichecker.lib.base import BaseController, render
from yubichecker.lib import xtea
from yubichecker.lib.yubikey import decrypt as yubi_decrypt
from yubichecker.lib.signature import generate_api

log = logging.getLogger(__name__)

class AddkeyController(BaseController):

  def __init__(self):
    self.xtea_key = config['xtea_key']

  def index(self, msg=None):
    c.err = msg
    c.user = False
    if 'user' in session:
      c.user = session['user']
    return render('/addkey/index.html')

  def do(self):

    if 'otps' not in request.params or 'aes' not in request.params or 'mail' not in request.params :
      redirect_to(action="index", msg='All fields are requiered')
    
    if request.params['otps'] == '' or request.params['aes'] == '' or request.params['mail'] == '' :
      redirect_to(action='index', msg='All fields are requested')

    aes  = request.params['aes'].strip()
    otps = request.params['otps'].strip().split('\n')
    mail = request.params['mail'].strip()

    # check: is this email already in our system ? if so, is the user registered? if so, are the email addresses the same ?
    c = Session.query(Key).filter(Key.email == mail)
    if c.count() != 0:
      if 'user' not in request.params:
        redirect_to(action='index', msg='This email address is already registered, please use the <a href="/manager">manager</a> to add this key.')
        pass
      if request.params['user'] != mail:
        redirect_to(action='index', msg = 'This is NOT your email address')
        pass

    # check how many OTPs there are
    if len(otps) < 3:
      redirect_to(action='index', msg='We need at least 3 OTPs')

    # check AES length
    if not yubi_decrypt.RE_AES_KEY.match(aes):
      redirect_to(action='index', msg='BAD AES Key')

    # check how many OTP there are

    for otp in otps:
      if otp:
        try:
          data = yubi_decrypt.YubikeyToken(otp.strip(), aes)
        except yubi_decrypt.InvalidToken:
          redirect_to(action="index", msg="Bad OTP - at least one is wrong!")

    secret_id = data.secret_id
    public_id = data.public_id

    # get API key if one already exists
    api = Session.query(Key).filter(Key.email == mail)
    if api.count() > 0:
      c.replay = True
      api_key = api[0].api.key
    else:
      c.replay = False
      api_key = generate_api()

    # crypt AES key
    crypted = xtea.crypt(self.xtea_key, aes).encode('hex')

    # last check : is this AES unique ?
    if Session.query(id_AES).filter(id_AES.aes == crypted).count() != 0:
      redirect_to(action="index", msg="Bad AES - Please generate a new one.")

    # create new key object
    key = Key()
    key.private_id   = secret_id
    key.public_id    = public_id
    key.email        = mail

    # create new key - AES part
    new_aes     = id_AES()
    new_aes.aes = crypted
    Session.add(new_aes)
    Session.commit()
    id_aes = Session.query(id_AES).filter(id_AES.aes == crypted).one().id
    # add ID to key
    key.id_aes       = id_aes

    # create new key - API part
    if c.replay:
      key.api_key = api[0].api.id
    else:
      api = API()
      api.key = api_key
      Session.add(api)
      Session.commit()
      api_id = Session.query(API).filter(API.key == api_key).one().id
      key.api_key = api_id

    Session.add(key)
    Session.commit()
    
    c.api_key = api_key
    
    return render('/addkey/success.html')
