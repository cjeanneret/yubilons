import logging

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from yubichecker.lib.base import BaseController, render
from yubichecker.lib import xtea
from yubichecker.lib.yubikey import decrypt as yubi_decrypt
from yubichecker.lib.signature import generate_api
from yubichecker.model import *
from yubichecker.lib.verify import check_yubikey

from sqlalchemy import and_, or_


log = logging.getLogger(__name__)

class ManagerController(BaseController):

  def __before__(self, action):
    self.xtea_key = config['xtea_key']
    if 'user' not in session and action not in ['login', 'logup']:
      redirect_to(action='login')
    if 'user' in session:
      self.user = session['user']
    pass

  def __init__(self):
    pass

  def index(self):

    c.keys = Session.query(Key).filter(Key.email == self.user).all()
    return render('/manager/index.html')

  def login(self):
    return render('/manager/login.html')

  def logup(self):
    if 'mail' not in request.params or 'otp' not in request.params:
      redirect_to(action='login')
    
    otp = request.params['otp']
    mail = request.params['mail']

    check = check_yubikey(otp, False, self.xtea_key,True)
    
    if check:
      if check.email == mail:
        session['user'] = check.email
        session.save()
        redirect_to(action='index')
        pass
      pass
    redirect_to(action='login')
    pass

  def logout(self):
    return 'logout'

  def manage(self, key_id=None):
    key = Session.query(Key).filter(and_(Key.email == self.user, Key.id == key_id))
    if key.count() == 1:
      c.key = key.one()
      return render('/manager/manage.html')
    else:
      redirect_to(action='index')
      pass
    pass

  def update(self, key_id=None):
    key = Session.query(Key).filter(and_(Key.email == self.user, Key.id == key_id))
    if key.count() == 1:
      key = key.one()
      key.yubi_aes.aes = request.params['aes']
      Session.flush()
      Session.commit()
    redirect_to(action="index")
    pass

  def revoque(self, key_id):
    key = Session.query(Key).filter(and_(Key.email == self.user, Key.id == key_id))
    if key.count() == 1:
      c.key = key.one()
      return render('/manager/revoque.html')
    else:
      redirect_to(action='index')
      pass
    pass

  def dorevoque(self, key_id):
    key = Session.query(Key).filter(and_(Key.email == self.user, Key.id == key_id))
    if key.count() == 1:
      key = key.one()
      aes = key.yubi_aes.id
      Session.delete(key)
      Session.delete(Session.query(id_AES).filter(id_AES.id == aes).one())
      Session.commit()
      
    redirect_to(action='index')
    pass
