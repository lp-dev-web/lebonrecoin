from django import forms
from django.utils.translation import gettext_lazy as _
from app.models import Product, Categorie, State, Picture


class AdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("categorie", "title", "price", "description", "state")

    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        initial=0,
        label=_("Categorie"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    title = forms.CharField(
        label=_("Title"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            {"class": "form-control", "placeholder": _("Title of the ad")}
        ),
    )
    price = forms.CharField(
        label=_("Price"),
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "10"}),
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=1000,
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": _("Description of the ad")}
        ),
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        initial=0,
        label=_("State"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ("picture_1", "picture_2", "picture_3")

    picture_1 = forms.ImageField(
        label=_("Picture 1"),
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control p-1"}),
    )
    picture_2 = forms.ImageField(
        label=_("Picture 2"),
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control p-1"}),
    )
    picture_3 = forms.ImageField(
        label=_("Picture 3"),
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control p-1"}),
    )

    def clean_picture_1(self):
        picture_1 = self.cleaned_data["picture_1"]
        if picture_1 is None:
            raise forms.ValidationError(_("You must add at least one image."))
        return picture_1


class EditPictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ("picture_1", "picture_2", "picture_3")

    picture_1 = forms.ImageField(
        label=_("Picture 1"),
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control p-1"}),
    )
    picture_2 = forms.ImageField(
        label=_("Picture 2"),
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control p-1"}),
    )
    picture_3 = forms.ImageField(
        label=_("Picture 3"),
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control p-1"}),
    )
