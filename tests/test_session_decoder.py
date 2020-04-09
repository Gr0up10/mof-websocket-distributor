from app.session_decoder import decode


def test_decode():
    decoded = decode('NzdiYjg3NmQzOTBkZDc1ZDZiYWUyOGNmYWE0ZDI1NmQwNjFiMjA3ZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxMjhmMTBhMGZmMWNiOTU5NzM4YmU2YmJlYmQ0YzAyMDQ4NThkOWM0In0=', 'ecw==078()bm0#u^f6))--6jz3nk27rwy04wb6=2f_3rqrsvq*')
    assert decoded['_auth_user_id'] == '1'
    assert decoded['_auth_user_backend'] == 'django.contrib.auth.backends.ModelBackend'
    assert decoded['_auth_user_hash'] == '128f10a0ff1cb959738be6bbebd4c0204858d9c4'
