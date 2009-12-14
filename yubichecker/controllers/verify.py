import logging, re
from datetime import datetime

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from yubichecker.lib.base import BaseController, render
#from yubichecker.lib import xtea
#from yubichecker.lib.signature import *
#from yubichecker.lib.yubikey import decrypt as yubi_decrypt
from yubichecker.lib.verify import check_yubikey

from yubichecker.model import *

log = logging.getLogger(__name__)

class VerifyController(BaseController):

  def __init__(self):
    self.RE_TOKEN = re.compile(r'^[cbdefghijklnrtuv]{32,64}$')
    self.xtea_key = config['xtea_key']

  def index(self):
    return render('/verify/index.html')

  def check(self):
    response.headers['content-type'] = 'text/plain;name=yubico.txt'
    now = datetime.now()
    h = False
    
    if 'otp' in request.params:
      otp = request.params['otp']
    else:
      output = '''status=NO_OTP
t=%s''' % now
      return output

    if not self.RE_TOKEN.match(otp):
      output = '''status=BAD_OTP
t=%s''' % now
      return output

    if 'h' in request.params:
      h = request.params['h']

    return check_yubikey(otp, h, self.xtea_key)
