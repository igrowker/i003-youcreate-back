import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CustomPasswordValidator(serializers.ModelSerializer):
    def validate(self, password, user=None):
        """
        Validate that the password is not too common or a variant of the username.

        If the password is valid, return ``None``.
        If the password is invalid, raise ValidationError with all error messages.
        """
        regex = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
        if not password or not isinstance(password, str):
            raise ValidationError(
                _(
                    "La contraseña debe tener al menos 8 caracteres, una letra mayúscula y un número."
                ),
                code="password_invalid",
            )
        if not re.match(regex, password):
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres, "
                "una letra mayúscula y un número.",
                code="password_invalid",
            )
