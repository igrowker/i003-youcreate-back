import pyotp
from django.core.mail import send_mail


def send_otp_via_email(user):
    print("Insisde send_otp_via_email")
    print(get_otp_code(user))
    otp_code = get_otp_code(user)  # Obtener el código OTP
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

def generate_otp_secret(user):
    print("Insisde generate_otp_secret")
    user.otp_secret = pyotp.random_base32()  # Generar secreto OTP
    user.save()

# Cambiar el valor intervalo a lo que necesites, e.g., 60
def get_otp_code(user, interval=120):
    print("Insisde get_otp_code")
    if not user.otp_secret:  # Si no tiene secreto, no puede obtener el código OTP
        print("No tiene secreto")
        user.generate_otp_secret()
    # Crear TOTP con el secreto
    totp = pyotp.TOTP(user.otp_secret, interval=interval)
    print(totp.now())
    return totp.now()  # Obtener el código OTP