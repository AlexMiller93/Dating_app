from django.contrib.auth.models import BaseUserManager 


class UserCustomManager(BaseUserManager):

    def create_user(self, email, password=None, *args, **kwargs):
        
        if not email:
            raise TypeError('Пользователь должен иметь email')

        user = self.model(
            email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, *args, **kwargs):

        if password is None:
            raise TypeError('Cуперпользователь должен иметь пароль')

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user
    
    