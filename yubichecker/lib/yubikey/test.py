"""
    Basic tests
"""

import decrypt

DEBUG = False

test_cases = [
    {
        'description': 'Testing the most common case that should succeed',
        'should_succeed': True,
        'aes_key': '0123456789abcdef0123456789abcdef',
        'otp': 'cbdefghijklnbvhgbhebfuurheknkvulgtdejrljhifn',
        'public_id': 'cbdefghijkln',
        'secret_id': 'ab1234512345',
        'counter':  41345,
        'counter_session': 244,
        'timestamp': 12123456,
        'random_number': 32999
    },
    {
        'description': 'A shorter than normal public_id should also be possible',
        'should_succeed': True,
        'aes_key': '0123456789abcdef0123456789abcdef',
        'otp': 'cbdbvhgbhebfuurheknkvulgtdejrljhifn',
        'public_id': 'cbd',
        'secret_id': 'ab1234512345',
        'counter':  41345,
        'counter_session': 244,
        'timestamp': 12123456,
        'random_number': 32999
    },
    {
        'description': 'A too long OTP value',
        'should_succeed': False,
        'aes_key': '0123456789abcdef0123456789abcdef',
        'otp': 'cbdefghijklnbvhgbhebfuurheknkvulgtdejrljhifncbdefghijklnbvhgbhebfuurheknkvulgtdejrljhifn',
        'public_id': 'cbdefghijkln',
        'secret_id': 'ab1234512345',
        'counter':  41345,
        'counter_session': 244,
        'timestamp': 12123456,
        'random_number': 32999
    },
    {
        'description': 'Wrong character in OTP value',
        'should_succeed': False,
        'aes_key': '0123456789abcdef0123456789abcdef',
        'otp': 'cadefghijklnavhgaheafuurheknkvulgtdejrljhifn',
        'public_id': 'cbdefghijkln',
        'secret_id': 'ab1234512345',
        'counter':  41345,
        'counter_session': 244,
        'timestamp': 12123456,
        'random_number': 32999
    },
    {
        'description': 'A too short AES key',
        'should_succeed': False,
        'aes_key': '012345678abcdef0123456789abcdef',
        'otp': 'cbdbvhgbhebfuurheknkvulgtdejrljhifn',
        'public_id': 'cbdefghijkln',
        'secret_id': 'ab1234512345',
        'counter':  41345,
        'counter_session': 244,
        'timestamp': 12123456,
        'random_number': 32999
    },
    {
        'description': 'Wrong character in AES key',
        'should_succeed': False,
        'aes_key': 'X123456789abcdef0123456789abcdef',
        'otp': 'cbdefghijklnbvhgbhebfuurheknkvulgtdejrljhifn',
        'public_id': 'cbdefghijkln',
        'secret_id': 'ab1234512345',
        'counter':  41345,
        'counter_session': 244,
        'timestamp': 12123456,
        'random_number': 32999
    },
]

print '\nTesting Yubico-python library...\n'

ok_counter = 0
fail_counter = 0

for tc in test_cases:
    print u'%s:' % tc['description']

    success = True
    
    try:
        yubikey = decrypt.YubikeyToken(tc['otp'], tc['aes_key'])
    except Exception, e:
        print e
        success = False
    else:
        if yubikey.crc_ok:

            for key, value in tc.items():
                if not key in ('aes_key', 'otp', 'description', 'should_succeed'):
                    if DEBUG:
                        print '    - %s = %s' % (key, getattr(yubikey, key))
                    if getattr(yubikey, key) == value:
                        if DEBUG:
                            print '    - %s value is OK' % key
                    else:
                        success = False
                        print '    - ERROR: %s value is NOT the same' % key
        else:
            success = False
            print '    - ERROR: CRC check NOT ok'

    if tc['should_succeed']:
        if success:
            print 'OK, test case succeeded when it should succeed.\n'
            ok_counter += 1
        else:
            print 'FAILED, test case failed that should succeed.\n'
            fail_counter += 1
    else:
        if success:
            print 'FAILED, test case succeeded when it shouldn\'t.\n'
            fail_counter += 1
        else:
            print 'OK, test case failed when it should faild.\n'
            ok_counter += 1

print 'Tests ok: %d' % ok_counter
print 'Tests failed: %d' % fail_counter

print 'Done\n'
