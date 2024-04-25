import phonenumbers
from django import forms

from app.models import Client, Lawyer, Case


class ClientForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Client
        fields = ["image", "name", "surname", "birthdate", "phone", "email"]
        labels = {
            "image": "Your photo",
            "name": "Name",
            "surname": "Surname",
            "Birthdate": "Birthdate",
            "phone": "Phone",
            "email": "Email",
        }

    def clean_name(self):
        client_name = self.cleaned_data["name"]
        if len(client_name) < 1:
            raise forms.ValidationError("Name is too short")

        if len(client_name) > 50:
            raise forms.ValidationError("Name is too long")

        if any(char.isdigit() for char in client_name):
            raise forms.ValidationError("Name must not contain digits")

        if client_name[0].islower():
            change_name = client_name.capitalize()
            self.cleaned_data["name"] = change_name

        if any(char.isupper() for char in client_name[0:]):
            changed_name = client_name.capitalize()
            self.cleaned_data["name"] = changed_name

        return client_name

    def clean_surname(self):
        client_surname = self.cleaned_data["surname"]
        if len(client_surname) < 1:
            raise forms.ValidationError("Surname is too short")

        if len(client_surname) > 50:
            raise forms.ValidationError("Surname is too long")

        if any(char.isdigit() for char in client_surname):
            raise forms.ValidationError("Surname is too long")

        if client_surname[0].islower():
            change_surname = client_surname.capitalize()
            self.cleaned_data["surname"] = change_surname

        if any(char.isupper() for char in client_surname[0:]):
            change_surname = client_surname.capitalize()
            self.cleaned_data["surname"] = change_surname

        return client_surname

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            raise forms.ValidationError("Phone cannot be empty")

        if len(phone) < 9:
            raise forms.ValidationError("The number provided is too short")

        try:
            parsed = phonenumbers.parse(phone, None)
        except phonenumbers.NumberParseException as error:
            raise forms.ValidationError(f"{error.args[0]}")

        formatted_phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return formatted_phone


class LawyerForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Lawyer
        fields = [
            "image",
            "name",
            "surname",
            "birthdate",
            "experience",
            "successful_cases",
            "unsuccessful_cases",
            "price",
            "characterization",
        ]
        labels = {
            "image": "Your photo",
            "name": "Name",
            "surname": "Surname",
            "birthdate": "Birthday",
            "experience": "Experience",
            "successful_cases": "Successful cases",
            "unsuccessful_cases": "Unsuccessful cases",
            "price": "Price",
            "characterization": "Characterization",
        }

    def clean_name(self):
        lawyer_name = self.cleaned_data["name"]
        if len(lawyer_name) < 1:
            raise forms.ValidationError("Name is too short")

        if len(lawyer_name) > 50:
            raise forms.ValidationError("Name is too long")

        if any(char.isdigit() for char in lawyer_name):
            raise forms.ValidationError("Name must not contain digits")

        if lawyer_name[0].islower():
            change_name = lawyer_name.capitalize()
            self.cleaned_data["name"] = change_name

        if any(char.isupper() for char in lawyer_name[0:]):
            changed_name = lawyer_name.capitalize()
            self.cleaned_data["name"] = changed_name

        return lawyer_name

    def clean_surname(self):
        lawyer_surname = self.cleaned_data["surname"]
        if len(lawyer_surname) < 1:
            raise forms.ValidationError("Surname is too short")

        if len(lawyer_surname) > 50:
            raise forms.ValidationError("Surname is too long")

        if any(char.isdigit() for char in lawyer_surname):
            raise forms.ValidationError("Surname is too long")

        if lawyer_surname[0].islower():
            change_surname = lawyer_surname.capitalize()
            self.cleaned_data["surname"] = change_surname

        if any(char.isupper() for char in lawyer_surname[0:]):
            change_surname = lawyer_surname.capitalize()
            self.cleaned_data["surname"] = change_surname

        return lawyer_surname

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 100:
            raise forms.ValidationError("The price of services cannot be less than 100")

        return price


class ClientCaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["lawyer", "client", "article", "description"]
        labels = {
            "article": "Article",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lawyer"].widget = forms.HiddenInput()
        self.fields["client"].widget = forms.HiddenInput()
        self.fields["lawyer"].initial = kwargs.get("initial", {}).get("lawyer")
        self.fields["client"].initial = kwargs.get("initial", {}).get("client")

    def clean_article(self):
        article = self.cleaned_data["article"]
        if len(article) > 255:
            raise forms.ValidationError("Article is too long")

        return article


class LawyerCaseForm(ClientCaseForm):
    class Meta:
        model = Case
        fields = ["is_active", "lawyer", "client", "case_closed_successfully", "article", "description"]
        labels = {
            "article": "Article",
            "description": "Description",
        }

    def clean_article(self):
        article = self.cleaned_data["article"]
        if len(article) > 255:
            raise forms.ValidationError("Article is too long")

        return article


class EditLawyerForm(LawyerForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["successful_cases"].widget = forms.HiddenInput()
        self.fields["unsuccessful_cases"].widget = forms.HiddenInput()
        self.fields["successful_cases"].initial = kwargs.get("initial", {}).get("successful_cases")
        self.fields["unsuccessful_cases"].initial = kwargs.get("initial", {}).get("unsuccessful_cases")
