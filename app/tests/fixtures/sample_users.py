from pyflutterflow.auth import FirebaseUser

quill = FirebaseUser(**{
    "uid": "iamquill",
    "email": "quill@email.com",
    "role": "user",
    "name": "Quill",
    "email_verified": True,
    "auth_time": 13532456,
    "iat": 245256456,
    "exp": 534565345,
})

rocket = FirebaseUser(**{
    "uid": "imrocket",
    "email": "rocket@email.com",
    "role": "user",
    "name": "Rocket",
    "email_verified": True,
    "auth_time": 15325345,
    "iat": 34535453,
    "exp": 45464567,
})

admin = FirebaseUser(**{
    "uid": "iamadmin",
    "email": "admin@email.com",
    "name": "Admin User",
    "role": "admin",
    "email_verified": True,
    "auth_time": 34534534,
    "iat": 34534534,
    "exp": 34534534,
})
