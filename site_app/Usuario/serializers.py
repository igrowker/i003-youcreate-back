
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    pass
    correo = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "correo",
            "password",
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
            "correo": {"required": True},
            "pais_residencia": {"required": True},
            "redes_sociales": {"required": True},
            "telefono": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
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
            correo=validated_data.get("correo"),
            password=validated_data.get("password"),
            pais_residencia=validated_data.get("pais_residencia"),
            redes_sociales=validated_data.get("redes_sociales", []),
            telefono=validated_data.get("telefono"),
        )

        usuario.set_password(validated_data["password"])
        usuario.save()

        return usuario


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        usuario = CustomUser.objects.get(id=user.id)
        token = super(CustomTokenObtainPairSerializer, cls).get_token(usuario)
        print(token)
        # Add custom claims
        token["id"] = usuario.id
        token["pais"] = usuario.pais_residencia
        return token

