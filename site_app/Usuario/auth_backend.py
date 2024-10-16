import re

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CustomPasswordValidator(serializers.ModelSerializer):
    def validate(self, password, user=None):
        # Ensure the password is at least 8 characters long
        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code="password_too_short",
            )

        # Ensure the password has at least one uppercase letter
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("La contraseña debe tener al menos una letra mayúscula."),
                code="password_no_uppercase",
            )

        # Ensure the password has at least one number
        if not re.search(r"[0-9]", password):
            raise ValidationError(
                _("La contraseña debe tener al menos un número."),
                code="password_no_number",
            )

    def get_help_text(self):
        return _(
            "La contraseña debe tener al menos 8 caracteres, una letra mayúscula y un número."
        )
