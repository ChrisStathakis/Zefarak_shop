from django.core.exceptions import ValidationError

def validate_positive_decimal(value):
    if value < 0:
        return ValidationError('This number is negative!')
    return value