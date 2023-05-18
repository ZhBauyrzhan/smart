from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email: models.EmailField,
                    first_name: models.CharField,
                    last_name: models.CharField,
                    username: models.CharField
                    ):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email: models.EmailField,
                         first_name: models.CharField,
                         last_name: models.CharField,
                         username: models.CharField,
                         password: str):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        return user

    def active(self):
        return self.filter(is_active=True)
