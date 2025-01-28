import json
import time

from bittensor import Keypair
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Neuron


class HotkeyAuthentication(BaseAuthentication):

    def authenticate(self, request: HttpRequest) -> tuple[AbstractBaseUser, str]:
        method = request.method.upper()
        hotkey = request.headers.get("Hotkey")
        nonce = request.headers.get("Nonce")
        signature = request.headers.get("Signature")
        if not hotkey or not nonce or not signature:
            raise AuthenticationFailed("Missing authentication headers.")

        if abs(time.time() - float(nonce)) > int(settings.SIGNATURE_EXPIRE_DURATION):
            raise AuthenticationFailed("Invalid nonce")

        if not Neuron.objects.filter(hotkey=hotkey, is_active_validator=True).exists():
            raise AuthenticationFailed("Unauthorized hotkey.")

        client_headers = {
            "Nonce": nonce,
            "Hotkey": hotkey,
            "Note": request.headers.get("Note"),
            "SubnetID": request.headers.get("SubnetID"),
            "Realm": request.headers.get("Realm"),
        }
        client_headers = {k: v for k, v in client_headers.items() if v is not None}
        headers_str = json.dumps(client_headers, sort_keys=True)

        url = request.build_absolute_uri()
        data_to_sign = f"{method}{url}{headers_str}"

        if "file" in request.FILES:
            uploaded_file = request.FILES["file"]
            file_content = uploaded_file.read()
            decoded_file_content = file_content.decode(errors="ignore")
            data_to_sign += decoded_file_content

        try:
            is_valid = Keypair(ss58_address=hotkey).verify(
                data=data_to_sign.encode(), signature=bytes.fromhex(signature)
            )
        except Exception as exc:
            raise AuthenticationFailed(f"Signature verification failed: {exc}") from exc

        if not is_valid:
            raise AuthenticationFailed("Invalid signature.")

        return get_user_model(), hotkey
