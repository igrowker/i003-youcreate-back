from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Usuario.models import CustomUser



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "nombre",
        "apellido",
        "correo",
        "telefono",
        "password",
        "verificado",
        "pais_residencia",
        "redes_sociales",
        "activo",
    )
    list_filter = ("verificado", "activo")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nombre",
                    "apellido",
                    "correo",
                    "telefono",
                    "password",
                    "verificado",
                    "pais_residencia",
                    "redes_sociales",
                    "activo",
                )
            },
        ),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "nombre",
                "apellido",
                "correo",
                "password1",
                "password2",
                "verificado",
                "pais_residencia",
                "redes_sociales",
                "activo",
            ),
        },
    )


admin.site.register(CustomUser, CustomUserAdmin)
