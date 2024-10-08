import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL_DEV = "http://localhost:8000/"
BASE_URL_PRODUCTION = ""

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "RENDER" not in os.environ

ALLOWED_HOSTS = []
# Añade el host de Render a "ALLOWED_HOSTS" si existe
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

SITE_ID = 1  # Necessary for allauth

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:4200",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "Usuario",
    "Colaborador",
    "Ingreso",
    "PagoColaborador",
    "ObligacionFiscal",
    "ActionLog",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.mfa",
    # 'allauth.headless',
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.apple",
    "dj_rest_auth.registration",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
}

# Simple JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        # TODO: Change back to 5 minutes for production
        minutes=9999999
    ),  # Sets the expiration time of the access token
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=15
    ),  # Sets the expiration time of the refresh token
    "ROTATE_REFRESH_TOKENS": True,  # Automatically rotates the refresh tokens every time a new access token is generated
    "BLACKLIST_AFTER_ROTATION": True,  # Automatically blacklists tokens that have expired or have been rotated
    # TODO: Add Cron job to flush blacklisted tokens
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",  # Hash algorithm used to sign the access and refresh tokens (HS256: Symmetric encryption)
    "SIGNING_KEY": os.getenv(
        "SECRET_KEY"
    ),  # Signing key used to sign the access and refresh tokens
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_OBTAIN_SERIALIZER": "Usuario.serializers.CustomTokenObtainPairSerializer",
}

# Django Rest Auth config
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "access",
    "JWT_AUTH_REFRESH_COOKIE": "refresh",
    "JWT_AUTH_REFRESH_COOKIE_PATH": "auth/token/refresh/",
    "JWT_AUTH_HTTPONLY": False,  # Makes sure refresh token is sent
    "JWT_TOKEN_CLAIMS_SERIALIZER": "Usuario.serializers.CustomTokenObtainPairSerializer",
    "JWT_AUTH_RETURN_EXPIRATION": True,
    "REGISTER_SERIALIZER": "Usuario.serializers.CustomRegisterSerializer",
    "LOGIN_SERIALIZER": "Usuario.serializers.CustomLoginSerializer",
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "LOGOUT_REDIRECT_URL": "auth/login/",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS headers Middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Django AllAuth Middleware
]

ROOT_URLCONF = "proyecto.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "Templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "proyecto.wsgi.application"

DATABASES = {
    # DEFAULT para desarrollo
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
    # DEFAULT para producción
    "default": dj_database_url.config(
        default="postgresql://postgres:Admin0000@localhost:5432/you_create_db",
        conn_max_age=600,
    )
}

AUTH_USER_MODEL = "Usuario.CustomUser"

# Django AllAuth settings
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # No need to sent POST request to confirmation link
ACCOUNT_LOGIN_BY_CODE_ENABLED = True

# HEADLESS_ONLY = True
# HEADLESS_FRONTEND_URLS = {
#     "account_confirm_email": "/account/verify-email/{key}",
#     "account_reset_password": "/account/password/reset",
#     "account_reset_password_from_key": "/account/password/reset/key/{key}",
#     "account_signup": "/account/signup",
#     "socialaccount_login_error": "/account/provider/callback",
# }

# Activa la autenticación multifactor con TOTP
MFA_SUPPORTED_TYPES = ["totp"]
MFA_TOTP_PERIOD = 60  # 1 minuto de duración para el código TOTP
MFA_ADAPTER = "allauth.mfa.adapter.DefaultMFAAdapter"
MFA_TOTP_ISSUER = "YouCreate"
# MFA default forms, se pueden cambiar los formularios usados en la autenticación multifactor
MFA_FORMS = {
    "authenticate": "allauth.mfa.base.forms.AuthenticateForm",
    "reauthenticate": "allauth.mfa.base.forms.AuthenticateForm",
    "activate_totp": "allauth.mfa.totp.forms.ActivateTOTPForm",
    "deactivate_totp": "allauth.mfa.totp.forms.DeactivateTOTPForm",
    "generate_recovery_codes": "allauth.mfa.recovery_codes.forms.GenerateRecoveryCodesForm",
}

# URLs
LOGIN_URL = "auth/login/"
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "localhost:4200/home"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "Usuario.auth_backend.CustomPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
]


# Django SMTP settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uidb64>/<token>/
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = (
    "http://localhost:8000/password-reset/confirm/"
)

ACCOUNT_EMAIL_VERIFICATION_SENT_REDIRECT_URL = (
    "auth/registration/email-verification/sent/"
)

# Social auth
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "key": "",  # leave empty, Google doesn't need a key for social auth
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    },
}
