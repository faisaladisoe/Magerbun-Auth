from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, username, role, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not role:
            raise ValueError('Users must have a role, either buyer or seller')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role.lower()
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, role, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
            role=role
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.passwordConfirmation = password

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # Required area
    email = models.EmailField(verbose_name='email address', max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=75)
    passwordConfirmation = models.CharField(max_length=75)
    ROLE_EXISTING = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller')
    ]
    role = models.CharField(verbose_name='role, either buyer or seller', max_length=7, choices=ROLE_EXISTING)

    # Optional Area
    namaLengkap = models.CharField(verbose_name='nama lengkap', max_length=150, null=True)
    namaPanggilan = models.CharField(verbose_name='nama panggilan', max_length=20, null=True)
    nomorInduk = models.CharField(verbose_name='nomor induk mahasiswa/pegawai', max_length=30, null=True, unique=True)
    nomorHP = models.CharField(verbose_name='nomor hp', max_length=15, null=True, unique=True)
    angkatan = models.CharField(max_length=5, null=True)
    jurusan = models.CharField(max_length=20, null=True)
    namaToko = models.CharField(verbose_name='nama toko', max_length=50, null=True, unique=True)
    DAGANGAN = [
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
        ('jajanan', 'Jajanan'),
        ('campuran', 'Campuran')
    ]
    tipeDagangan = models.CharField(verbose_name='tipe dagangan', max_length=10, null=True, choices=DAGANGAN)

    # Add-on area
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
