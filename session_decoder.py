import base64
import hashlib
import hmac
import json


def session_utoken(msg, secret_key, class_name='SessionStore'):
    key_salt = "django.contrib.sessions" + class_name
    sha1 = hashlib.sha1((key_salt + secret_key).encode('utf-8')).digest()
    utoken = hmac.new(sha1, msg=msg, digestmod=hashlib.sha1).hexdigest()
    return utoken


def decode(session_data, secret_key, class_name='SessionStore'):
    encoded_data = base64.b64decode(session_data)
    utoken, pickled = encoded_data.split(b':', 1)
    expected_utoken = session_utoken(pickled, secret_key, class_name)
    if utoken.decode() != expected_utoken:
        raise BaseException('Session data corrupted "%s" != "%s"',
                            utoken.decode(),
                            expected_utoken)
    return json.loads(pickled.decode('utf-8'))