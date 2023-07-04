import uuid
import random
import string
from PIL import Image
from io import BytesIO
from random import randint

from django.db import models
from django.core.files import File
from django.http.request import HttpRequest
from django.core.files.base import ContentFile


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


"""
To get unique id's according to the length of n
"""


def generate_unique_id(n):
    unique_id = []

    characters = list(string.ascii_letters + string.digits)
    random.shuffle(characters)

    for i in range(n):
        unique_id.append(random.choice(characters))
    random.shuffle(unique_id)

    return "".join(unique_id)


"""
To get random password according to the length of n
"""


def random_password(n):
    password = []

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)

    for i in range(n):
        password.append(random.choice(characters))
    random.shuffle(password)

    return "".join(password)


# function to join multiple serializer errors
def join_errors(_errors=[]):
    errors = {}
    for _error in _errors:
        if hasattr(_error, '_errors'):
            errors.update(_error._errors)

    return errors


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def is_valid_uuid(value):
    """
        to find the string is valid uuid 
    """
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False


def get_client_ip(request: HttpRequest)-> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def resize( imageField: models.ImageField | models.FileField, size:tuple):
    im = Image.open(imageField)  # Catch original
    source_image = im.convert('RGB')
    source_image.thumbnail(size)  # Resize to size
    output = BytesIO()
    source_image.save(output, format='JPEG') # Save resize image to bytes
    output.seek(0)

    content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
    file = File(content_file)

    random_name = f'{uuid.uuid4()}.jpeg'
    
    return (random_name,file)


def is_ajax(request:HttpRequest)-> bool:
    """
    ## To find the request is from ajax or normal http request
    - navigate - normal http request
    - cors     - ajax request
    """
    return request.META.get("HTTP_SEC_FETCH_MODE") == "cors"


def getDomain(request: HttpRequest)-> str:
    protocol = "http://"

    if request.is_secure():
        protocol = "https://"

    host = request.get_host()

    return protocol + host
