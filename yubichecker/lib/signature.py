import urllib2, base64, hmac
from hashlib import sha512
from random import seed, choice
from datetime import datetime
from yubichecker.model import *

def yubisign(key, s):
  args = hmac.new(key, s, digestmod=sha512)
  sign = base64.b64encode(args.digest())
  return sign

def yubisign_check(key, s, their_sign):
  args = hmac.new(key, s, digestmod=sha512)
  our_sign = base64.b64encode(args.digest())
  print our_sign
  print their_sign
  return (our_sign == their_sign)

def generate_api():
  __hexchar = '0123456789abcdef'
  __api_size = 20
  seed(datetime.now())
  api_key =  ''.join([choice(__hexchar) for x in xrange(__api_size)])
  if Session.query(API).filter(API.key == api_key).count() != 0:
    return generate_api()
  return api_key
