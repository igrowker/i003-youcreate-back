from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp #2fa

class CustomUser(AbstractUser):
    # OTP/2FA--------
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    is_mfa_enabled = models.BooleanField(default=True)

    def generate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()
        self.save()

    def get_otp_code(self, interval=120):  # Cambiar el valor intervalo a lo que necesites, e.g., 60
        if not self.otp_secret:
            self.generate_otp_secret()
        totp = pyotp.TOTP(self.otp_secret, interval=interval)
        return totp.now()
    # OTP/2FA--------
    class Roles(models.TextChoices):
        ADMIN = "Administrador"
        COLABORADOR = "Colaborador"
        USUARIO = "Usuario"

    # Crea los campos del modelo CustomUser
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    pais_residencia = models.CharField(max_length=255)
    redes_sociales = models.JSONField(null=True)
    numero_fiscal = models.CharField(max_length=25)
    monotributo = models.BooleanField(default=False)

    # Crea los campos adicionales usados para la autenticación con OTP/MFA
    # is_mfa_enabled = models.BooleanField(default=False)
    # otp_secret = models.CharField(max_length=16, blank=True, null=True)

    # Añade un campo para el rol del usuario
    role = models.CharField(
        max_length=255, choices=Roles.choices, default=Roles.USUARIO
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Remove los campos por defecto de Django
    username = None
    first_name = None
    last_name = None

    # Personalizar el campo USERNAME_FIELD para que sea el correo del usuario
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class UserManager(BaseUserManager):
    def create_user(self, email, password, nombre, apellido, **extra_fields):
        if not email:
            raise ValueError("Correo no puede estar vacío")
        if not nombre:
            raise ValueError("Nombre no puede estar vacío")
        if not apellido:
            raise ValueError("Apellido no puede estar vacío")

        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nombre, apellido):
        user = self.create_user(
            email, password=password, nombre=nombre, apellido=apellido
        )
        user.role = CustomUser.Roles.ADMIN
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
