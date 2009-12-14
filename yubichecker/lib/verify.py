from datetime import datetime
from yubichecker.lib.base import BaseController, render
from yubichecker.lib import xtea
from yubichecker.lib.signature import *
from yubichecker.lib.yubikey import decrypt as yubi_decrypt
from pylons.controllers.util import abort

def check_yubikey(otp, h, xtea_key,boolean=False):
    now = datetime.now()

    key_id = otp[0:12]
    yubi = Session.query(Key).filter(Key.public_id == key_id)

    if yubi.count() == 0:
      abort(404, "No key found!")

    yubik = yubi.one()
    xt = yubik.yubi_aes.aes.decode('hex')
    aes = xtea.crypt(xtea_key, xt)
    api_key = yubik.api.key


    # first of all: check signature if available
    if h and not yubisign_check(api_key, 'otp=%s'%otp, h):
      if boolean:
        return False
      else:
        abort(203, 'Bad signature')

    try:
      data = yubi_decrypt.YubikeyToken(otp, aes)
    except yubi_decrypt.InvalidAESKey:
      if boolean:
        return False
      else:
        abort(203, 'Invalid AES')
    except yubi_decrypt.InvalidToken:
      if boolean:
        return False
      else:
        output = '''status=BAD_OTP
t=%s''' % now
        sign = yubisign(api_key, output)
        return '%s\nh=%s' % (output, sign)

    if data.secret_id != yubik.private_id:
      if boolean:
        return False
      else:
        abort(203, '''It seems your key is the wrong one. Private IDs don't match!''')

    counter = data.counter + data.counter_session

    if counter <= yubik.increment:
      if boolean:
        return False
      else:
        output = '''status=REPLAYED_OTP
t=%s''' % now
        sign = yubisign(api_key, output)
        return '%s\nh=%s' % (output, sign)

    # ok, checks are done, all is green
    # let' update yubi for the increment part: take increment value from yubikey, and insert it
    yubik.increment = counter
    Session.flush()
    Session.commit()
    if boolean:
      return yubik

    output = '''status=OK
t=%s''' % now

    sign = yubisign(api_key, output)
    return '%s\nh=%s' % (output, sign)

