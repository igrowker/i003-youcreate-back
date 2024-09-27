from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import exceptions as url_exceptions

from proyecto import settings

from .auth_backend import CustomPasswordValidator
from .models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    """Serializer para registrar un usuario"""

    username = None
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[CustomPasswordValidator],  # [validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    nombre = serializers.CharField(required=True)
    apellido = serializers.CharField(required=True)
    pais_residencia = serializers.CharField(required=True)
    redes_sociales = serializers.JSONField(required=False, allow_null=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    numero_fiscal = serializers.CharField(required=True)

    def get_cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "nombre": self.validated_data.get("nombre", ""),
            "apellido": self.validated_data.get("apellido", ""),
            "pais_residencia": self.validated_data.get("pais_residencia", ""),
            "redes_sociales": self.validated_data.get("redes_sociales", {}),
            "telefono": self.validated_data.get("telefono", ""),
            "numero_fiscal": self.validated_data.get("numero_fiscal", ""),
        }

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
            "nombre",
            "apellido",
            "telefono",
            "pais_residencia",
            "redes_sociales",
        )
        extra_kwargs = {
            "nombre": {"required": True},
            "apellido": {"required": True},
            "email": {"required": True},
            "pais_residencia": {"required": True},
            "redes_sociales": {"required": True},
            "telefono": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Los campos de contraseña no coinciden"}
            )

        return attrs

    def create(self, validated_data):
        if not validated_data:
            raise ValueError("Validated data is empty")

        usuario = CustomUser.objects.create(
            nombre=validated_data.get("nombre"),
            apellido=validated_data.get("apellido"),
            email=validated_data.get("email"),
            password=validated_data.get("password1"),
            pais_residencia=validated_data.get("pais_residencia"),
            redes_sociales=validated_data.get("redes_sociales", {}),
            telefono=validated_data.get("telefono"),
            numero_fiscal=validated_data.get("numero_fiscal"),
        )

        usuario.set_password(validated_data["password1"])
        usuario.save()

        return usuario


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.EMAIL:
            print('Inside get_auth_user_using_allauth')
            return self._validate_email(email, password)

        # Authentication through username
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.USERNAME:
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)

    def validate(self, attrs):
        username = None
        email = attrs.get("email")
        password = attrs.get("password")
        user = self.get_auth_user(username, email, password)

        if not user:
            print('Inside not user')
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if "dj_rest_auth.registration" in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=email)

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        usuario = CustomUser.objects.get(id=user.id)
        token = super(CustomTokenObtainPairSerializer, cls).get_token(usuario)
        # Add custom claims
        token["pais"] = usuario.pais_residencia
        token["role"] = usuario.role
        return token
