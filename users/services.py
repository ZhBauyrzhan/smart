import random
import uuid
from typing import Protocol, OrderedDict

from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import tokens
from templated_email import send_templated_mail

from src import settings
from users import repos
from .models import CustomUser


class UserServicesInterface(Protocol):
    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> CustomUser | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        session_id = self._verify_email(data=data)
        return {
            'session_id': session_id,
        }

    def verify_user(self, data: OrderedDict):
        user_data = cache.get(data['session_id'])

        if not user_data:
            raise ValidationError

        if data['code'] != user_data['code']:
            raise ValidationError

        user = self.user_repos.create_user(data={
            'email': user_data['email']
        })
        self._send_letter_to_email(user=user)

    def create_token(self, data: OrderedDict) -> dict:
        session_id = self._verify_phone_number(data=data, is_exist=True)

        return {
            'session_id': session_id,
        }

    def verify_token(self, data: OrderedDict) -> dict:
        session = cache.get(data['session_id'])
        if not session:
            raise ValidationError

        if session['code'] != data['code']:
            raise ValidationError

        user = self.user_repos.get_user(data={'phone_number': session['phone_number']})
        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access),
            'refresh': str(refresh),
        }

    def _verify_email(self, data: OrderedDict, is_exists: bool = False) -> str:
        email = data['email']
        if is_exists:
            user = self.user_repos.get_user(data=data)
            email = str(user.email)

        code = self._generate_code()
        session_id = self._generate_session_id()

        cache.set(session_id, {'email': email, 'code': code, **data}, timeout=300)

        # TODO: Write send email code

        return session_id

    @staticmethod
    def _send_letter_to_email(user: CustomUser) -> None:
        send_templated_mail(
            template_name='Welcome',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            context={
                'email': user.email,
                'name': f'{user.first_name} {user.last_name}',
                'username': user.username
            },
        )

    @staticmethod
    def _generate_code(length: int = 6) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())
