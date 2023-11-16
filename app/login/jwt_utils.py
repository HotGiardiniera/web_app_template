import jwt
from typing import Dict

from app.settings import settings

settings = settings()


class JWTEncoder:
    """
    Basic JWT auth class
    Only decodes based on signing keys from a JWKS endpoint
    """
    def __init__(self, jwks_url: str, algorithm='RS256', audience=settings.base_url):
        self.jwk_client = jwt.PyJWKClient(jwks_url)
        self.header = {
            'kid': settings.jwt_kid
        }
        self.algorithm = algorithm
        self.audience = audience

    def encode(self, payload: Dict):
        payload['aud'] = self.audience
        return jwt.encode(
            payload,
            settings.jwt_private_key.get_secret_value(),
            algorithm=self.algorithm,
            headers=self.header
        )

    def decode(self, token: str):
        signing_key = self.jwk_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=[self.algorithm],
            audience=self.audience,
            options={"verify_exp": True},
        )


