import secrets
import string


def generate_secure_6_digit_code():
    digits = string.digits
    code = ''.join(secrets.choice(digits) for i in range(6))
    return code