import re

from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)
        path = reverse(
            "password_reset_confirm",
            args=[user_pk_to_url_str(user), temp_key],
        )

        for user in self.users:
            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            url_generator = kwargs.get("url_generator", default_url_generator)
            url = url_generator(request, user, temp_key)
            uid = user_pk_to_url_str(user)

            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
                "token": temp_key,
                "uid": uid,
                "path": path,
            }
            if (
                allauth_account_settings.AUTHENTICATION_METHOD
                != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
        return self.cleaned_data["email"]


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        # use the custom reset form
        self.reset_form = CustomAllAuthPasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value
