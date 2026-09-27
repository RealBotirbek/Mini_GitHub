from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    phone = models.CharField(
        max_length=13, unique=True,
        blank=True, null=True,
        validators=[MinLengthValidator(13)]
    )
    email = models.EmailField(
        unique=True, blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True, null=True
    )
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return f"{self.username}: {self.get_full_name()}"
