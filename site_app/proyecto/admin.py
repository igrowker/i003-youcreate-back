from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Usuario.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "nombre",
        "apellido",
        "email",
        "telefono",
        "password",
        "pais_residencia",
        "redes_sociales",
        "is_active",
        "monotributo",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nombre",
                    "apellido",
                    "email",
                    "telefono",
                    "password",
                    "pais_residencia",
                    "redes_sociales",
                    "numero_fiscal",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "is_active", "role")},
        ),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "email",
                "password",
                "password2",
            ),
        },
    )

    list_filter = ["is_active", "role"]


admin.site.register(CustomUser, CustomUserAdmin)
