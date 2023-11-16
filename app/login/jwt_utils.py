import datetime
import uuid

import jwt
from typing import Dict, Tuple, Any

from jwt import PyJWTError

from app.settings import settings

settings = settings()


class JWTError(Exception):
    pass


class JWTHandler:
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

    def _run_encode(self, payload) -> str:
        return jwt.encode(
            payload,
            settings.jwt_private_key.get_secret_value(),
            algorithm=self.algorithm,
            headers=self.header
        )

    def encode(self, payload: Dict) -> Tuple[str, str]:
        payload['aud'] = self.audience
        payload['exp'] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
        payload['iat'] = datetime.datetime.now(datetime.UTC)
        payload['type'] = "access"
        payload['token_id'] = str(uuid.uuid4())
        token = self._run_encode(payload)
        # Generate refresh token
        payload['exp'] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=60)
        payload['type'] = "refresh"
        refresh_token = self._run_encode(payload)

        return token, refresh_token

    def decode(self, token: str, verify_expired: bool = True) -> Any:
        signing_key = self.jwk_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=[self.algorithm],
            audience=self.audience,
            options={"verify_exp": verify_expired},
        )

    def refresh(self, token: str, refresh: str) -> Tuple[str, str]:
        """
        Refresh a given access token.
        TODO need to check a centralized datastore if the refresh token has already been used
        :param token: access token
        :param refresh: refresh token
        :return: new access/refresh token
        """
        # Ensure the old token is good
        try:
            payload = self.decode(token, verify_expired=False)
            refresh_payload = self.decode(refresh, verify_expired=True)
        except PyJWTError:
            return token, refresh
        if payload and payload['token_id'] != refresh_payload['token_id']:
            raise JWTError("Mismatched token Ids")
        if payload:
            token, refresh = self.encode(payload)
        return token, refresh
