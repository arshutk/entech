from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator



########################
## USER ACCOUNT MODEL ##
########################

class AccountManager(BaseUserManager):
    '''Custon Manager for Account Model'''

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email for account must be set')
        
        if not password:
            raise ValueError('Password must be set before setting up the account')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff as True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser as True')

        return self._create_user(email, password, **extra_fields)



class Account(AbstractBaseUser, PermissionsMixin):
    '''Account Model which will be extended by different User Models'''

    # choices for the state of an user account, is_active flag's value will later be changed according to status field
    class ACCOUNT_STATUS(models.IntegerChoices):
        BLOCKED = 0
        ACTIVE = 1
        PENDING = 2
    
    class USER_TYPE(models.TextChoices):
        CUSTOMER = 'customer'
        VENDOR = 'vendor'
        ADMIN = 'admin'
        CONTENT_CREATOR = 'content_creator'

    account_id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)

    join_date = models.DateTimeField(auto_now_add=True)

    ver_code_gen_date = models.DateTimeField(auto_now=True, null=True)
    ver_code = models.CharField(max_length=100)
    status = models.SmallIntegerField(choices=ACCOUNT_STATUS.choices, default=2)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    user_type = models.CharField(max_length=15, choices=USER_TYPE.choices)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    

    def __str__(self):
        return f'{self.email} | Active: {self.is_active}'