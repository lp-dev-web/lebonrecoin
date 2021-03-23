from datetime import date
from django import forms
from django.utils.translation import gettext_lazy as _
from app.models import User, Address, Countrie, Region, Citie
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "birth_date",
        )

    username = forms.CharField(
        label=_("Username"),
        help_text=_("20 characters or fewer. Letters, digits and @/./+/-/_ only."),
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your username")}
        ),
    )
    first_name = forms.CharField(
        label=_("First name"),
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your first name")}
        ),
    )
    last_name = forms.CharField(
        label=_("Name"),
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your name")}
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("example@example.com")}
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        help_text=_("Your password must contain at least 8 characters."),
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "****************"}
        ),
    )
    password2 = forms.CharField(
        label=_("Retype password"),
        help_text=_("Enter the same password as before, for verification."),
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "****************"}
        ),
    )
    birth_date = forms.DateField(
        label=_("Birth date"),
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This user already exists."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("Passwords must be equal."))
        return password2

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        today = date.today()
        if (birth_date.year + 18, birth_date.month, birth_date.day) > (
            today.year,
            today.month,
            today.day,
        ):
            raise forms.ValidationError(_("You must be 18 years old to register."))
        return birth_date


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.CharField(
        label=_("Username"),
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your username")}
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "****************"}
        ),
    )


class InformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "birth_date")

    username = forms.CharField(
        label=_("Username"),
        help_text=_("20 characters or fewer. Letters, digits and @/./+/-/_ only."),
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your username")}
        ),
    )
    first_name = forms.CharField(
        label=_("First name"),
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your first name")}
        ),
    )
    last_name = forms.CharField(
        label=_("Name"),
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your name")}
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("example@example.com")}
        ),
    )
    birth_date = forms.DateField(
        label=_("Birth date"),
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        today = date.today()
        if (birth_date.year + 18, birth_date.month, birth_date.day) > (
            today.year,
            today.month,
            today.day,
        ):
            raise forms.ValidationError(_("You must be 18 years old."))
        return birth_date


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("country", "region", "city", "address", "phone_number")

    country = forms.ModelChoiceField(
        queryset=Countrie.objects.all(),
        initial=0,
        label=_("Country"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        initial=0,
        label=_("Region"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    city = forms.ModelChoiceField(
        queryset=Citie.objects.all(),
        initial=0,
        label=_("City"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label=_("Address"),
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your address")}
        ),
    )
    phone_number = forms.RegexField(
        regex="^(0|\+33)[0-9]{9}$",
        label=_("Phone number"),
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "0123456789"}
        ),
    )

    def clean_region(self):
        if not Region.objects.filter(country_id=self.cleaned_data["country"]).exists():
            raise forms.ValidationError(
                _("The region does not correspond with the country.")
            )
        return self.cleaned_data["region"]

    def clean_city(self):
        if not Citie.objects.filter(
            region_id=self.data["region"], name=self.cleaned_data["city"]
        ).exists():
            raise forms.ValidationError(
                _("The city does not correspond with the region.")
            )
        return self.cleaned_data["city"]
