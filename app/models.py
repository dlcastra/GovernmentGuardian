from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255)

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

    def __str__(self):
        return f"ID: {self.id} | Lawyer: {self.name} {self.surname}"


class CaseForm(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="case_forms")
    description = models.TextField()
    article = models.CharField(max_length=255)


class Case(models.Model):
    is_active = models.BooleanField(default=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name="lawyer_cases")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_lawyer")
    case_closed_successfully = models.BooleanField()
    article = models.CharField(max_length=255)
    description = models.TextField(null=True)
