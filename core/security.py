import datetime
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt as jose
import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITM, set_up

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_auth_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
    )
    return jose.encode(to_encode, SECRET_KEY, algorithm=ALGORITM)


def decode_access_token(token: str) -> dict:
    try:
        encode_jwt = jose.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITM])
    except:
        encode_jwt = VerifyToken(token).verify()
        return encode_jwt
    return encode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid auth token')
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp


class VerifyToken():

    def __init__(self, token: str, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config = set_up()


        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        if self.scopes:
            result = self._check_claims(payload, 'scope', str, self.scopes.split(' '))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, 'permissions', list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == 'scope':
            payload_claim = payload[claim_name].split(' ')

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (f"Insufficient {claim_name} ({value}). You don't have "
                                  "access to this resource")
                return result
        return result

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im50OVI5WlhRdHkxOUd0NE1hNDhsaSJ9.eyJlbWFpbCI6ImJvdG9ub2prZTEyMzRAZ21haWwuY29tIiwiaXNzIjoiaHR0cHM6Ly9kZXYtZTNpM3k3eDdhMDZtam9ubS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDE4NDg2ODg5MzE3MTAxODg3OTgiLCJhdWQiOlsiaHR0cHM6Ly9tZWR1enplbi1mYXN0YXBpLmNvbSIsImh0dHBzOi8vZGV2LWUzaTN5N3g3YTA2bWpvbm0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY2NzIyMTA5NywiZXhwIjoxNjY3MzA3NDk3LCJhenAiOiI0UXFScllnUFV6eEdEY0tzcHlOem5uaWllTmZseEcyWSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.mJD9QkYsZtHzxX3i-z2J_Zw1vTItdWO3AQwSCujPyIyXzm0nOOcRQZw434TPqQGd6Gc9fZsYw2LpNI4ufjrLSaVqrikHD5It3CryqSoJ_w3RkkUeTKJs53USbZnJwxO728L7wUgMic3T4cVQB0A82p1-ZnVdXcndOHwpTIRUAoh1sgd1z2x6gl0WcLEilQt2v8ZHDJF6xV8UrvxJrvu_V76n6HbKYMDhgyIB21bp4sLxLocDdGIozyB_17zeiZGplIKkMx610DwxM1-2JzsAhUifa8Bz_Sbehk7oAkcPXZ7WkMaXD_pN9HcmrgB1Dy1pKN4ddDRCtPGUC5AAMVVQuw'

