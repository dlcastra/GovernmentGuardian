import os

from django.contrib.auth.models import User
from django.db import models

from core import settings


class Client(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255)
    image = models.ImageField(upload_to="images/", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_is_client")

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = os.path.join(settings.STATIC_URL, "default", "no_image.jpg")
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} | Client: {self.name} {self.surname}"


class Lawyer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthdate = models.DateField()
    experience = models.IntegerField()
    successful_cases = models.PositiveIntegerField(default=0)
    unsuccessful_cases = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField()
    characterization = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_is_lawyer")

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = os.path.join(settings.STATIC_URL, "default", "no_image.jpg")
        super(Lawyer, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} | Lawyer: {self.name} {self.surname}"


class Feedback(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="feedback")
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    lawyer = models.ForeignKey("Lawyer", on_delete=models.CASCADE, related_name="feedback")

    def __str__(self):
        return str(self.id)


class Case(models.Model):
    is_active = models.BooleanField(default=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name="lawyer_cases")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_lawyer")
    case_closed_successfully = models.BooleanField(default=False)
    article = models.CharField(max_length=255)
    description = models.TextField()
