from django.db import models
from django.contrib.auth.models import User
from django.db import models

from tools import logger


class Profile(models.Model):
    """
    models profile for add user image
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.BinaryField(null=True)
