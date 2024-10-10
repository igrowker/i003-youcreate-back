import pyotp
from django.core.mail import send_mail


def send_otp_via_email(user):
    otp_code = user.get_otp_code()  # Obtener el código OTP
    send_mail(
        "Tu código OTP",
        f"Tu código de verificación es {otp_code}",
        "igrowker.you.create@gmail.com",
        [user.email],
        fail_silently=False,  # No mostrar error si no se envía el correo
    )


def verify_otp(user, otp_code, interval=120):  # Verificar el código OTP
    if not user.otp_secret:  # Si no tiene secreto, no puede verificar
        return False
    # Crear TOTP con el secreto
    totp = pyotp.TOTP(user.otp_secret, interval=interval)
    return totp.verify(otp_code)  # Verificar el código OTP
