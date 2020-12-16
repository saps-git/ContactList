import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

"""
The JWT is just an authorization token that should be included in all requests:

The JWT is acquired by exchanging an username + password for an access token and an refresh token.
The access token is usually short-lived (expires in 5 min or so, can be customized though).
The refresh token lives a little bit longer (expires in 24 hours, also customizable). It is comparable to an authentication session. After it expires, you need a full login with username + password again.

Those are three distinctive parts that compose a JWT:

header.payload.signature

header
{
  "typ": "JWT",
  "alg": "HS256"
}

payload
{
  "token_type": "access",
  "exp": 1543828431,
  "jti": "7f5997b7150d46579dc2b49167097e7b",
  "user_id": 1
}

signature

The signature is issued by the JWT backend, using the header base64 + payload base64 + SECRET_KEY. 
Upon each request this signature is verified. If any information in the header or in the payload was changed by the client 
it will invalidate the signature. The only way of checking and validating the signature is by using your application’s SECRET_KEY. 
Among other things, that’s why you should always keep your SECRET_KEY secret!

"""


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request): # here we will write our login, based on which django will determine to authenticate or not
        auth_data = authentication.get_authorization_header(request) 

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ') #the incoming data will be in byte format, it will convert into native python format, and split accordingly (key, token)

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY) #decoding the token with help of the JWT_SECRET_KEY (signature), which is present in the settings file

            user = User.objects.get(username=payload['username']) #fetching the User details, of the given username
            return (user, token)

        except jwt.DecodeError as identifier:
            raise  exceptions.AuthenticationFailed('Invalid Login Credentials')
        except  jwt.ExpiredSignatureError as identifier:
            raise  exceptions.AuthenticationFailed('Session expired, please login again')
        return super().authenticate(request)