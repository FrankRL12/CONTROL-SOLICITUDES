from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, password, departamento=None):
        if not username:
            raise ValueError('el usuario debe tener un username')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            departamento=departamento
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, password):
        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    departamento = models.CharField(max_length=100, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    def __str__(self):
        return self.username
    



