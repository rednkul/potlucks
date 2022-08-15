from .models import PhoneNumber, Email, Address, AboutUs

def get_phone(request):

    if PhoneNumber.objects.filter(role='PRIMARY').exists():
        phone = PhoneNumber.objects.filter(role='PRIMARY').first().format_number()
    else:
        phone = ''

    return {
        'phone': phone
    }


def get_email(request):
    if Email.objects.filter(role='PRIMARY').exists():
        email = Email.objects.filter(role='PRIMARY').first().email
    else:
        email = ''

    return {
        'email': email
    }

def get_address(request):

    if Address.objects.filter(role='PRIMARY').exists():
        address = Address.objects.filter(role='PRIMARY').first().name
    else:
        address = ''
    return {
        'address': address
    }

def about_us(request):
    if AboutUs.objects.filter(role='PRIMARY').exists():
        about_us = AboutUs.objects.filter(role='PRIMARY').first().text
    else:
        about_us = ''
    return {
        'about_us': about_us
    }
