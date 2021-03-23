from django.contrib.messages.views import SuccessMessageMixin
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    DetailView,
    RedirectView,
    FormView,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
)
from django.utils.translation import gettext_lazy as _
from app.forms.account import RegisterForm, InformationForm, AddressForm, LoginForm
from app.models import User, Address, Favorite, Picture


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "account/authentication/form.html"
    model = User
    form_class = RegisterForm
    success_message = _("Your account has been created! You must now login.")
    success_url = reverse_lazy("login")

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("profil"))
        else:
            return super().get(request)

    def get_context_data(self, **kwargs):
        data = super(RegisterView, self).get_context_data(**kwargs)
        data["register_form"] = True
        data["title"] = _("Register")
        data["subtitle"] = _("Join a community of active users!")
        data["account"] = _("Have an account?")
        data["title_link"] = _("Login")
        data["link"] = "login"
        return data


class LoginView(FormView):
    template_name = "account/authentication/form.html"
    model = User
    form_class = LoginForm

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("profil"))
        else:
            return super().get(request)

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)

    def post(self, request, **kwargs):
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy("profil"))
        else:
            messages.warning(request, _("The username or password is incorrect."))
        return super().get(request)

    def get_context_data(self, **kwargs):
        data = super(LoginView, self).get_context_data(**kwargs)
        data["title"] = _("Login")
        data["subtitle"] = _("Login to discover all our features!")
        data["account"] = _("No account?")
        data["title_link"] = _("Sign in")
        data["link"] = "register"
        return data


class ProfilView(TemplateView):
    template_name = "account/profil.html"
    model = User


class ViewInformationView(DetailView):
    template_name = "account/information/account.html"
    model = User

    def get(self, request, *args, **kwargs):
        if self.kwargs["pk"] != self.request.user.pk:
            return HttpResponseRedirect(
                reverse_lazy("view-information", kwargs={"pk": self.request.user.pk})
            )
        else:
            return super().get(request)


class EditInformationView(SuccessMessageMixin, UpdateView):
    template_name = "account/form.html"
    model = User
    form_class = InformationForm
    success_message = _("Your information has been modified.")

    def get(self, request, *args, **kwargs):
        if self.kwargs["pk"] != self.request.user.pk:
            return HttpResponseRedirect(
                reverse_lazy("edit-information", kwargs={"pk": self.request.user.pk})
            )
        else:
            return super().get(request)

    def get_context_data(self, **kwargs):
        data = super(EditInformationView, self).get_context_data(**kwargs)
        data["title"] = _("Edit your information")
        data["link"] = "view-information"
        data["value"] = self.request.user.id
        data["button"] = _("Edit")
        return data

    def get_success_url(self):
        return reverse_lazy("view-information", kwargs={"pk": self.request.user.pk})


class NewAddressView(SuccessMessageMixin, CreateView):
    template_name = "account/form.html"
    model = Address
    form_class = AddressForm
    success_message = _("Your address has been registered.")

    def get(self, request, **kwargs):
        address = Address.objects.filter(user=self.request.user)
        if address.exists():
            return HttpResponseRedirect(
                reverse_lazy(
                    "view-address",
                    kwargs={"pk": address.get(user=self.request.user).pk},
                )
            )
        else:
            return super().get(request)

    def get_context_data(self, **kwargs):
        data = super(NewAddressView, self).get_context_data(**kwargs)
        data["title"] = _("Add your address")
        data["link"] = "view-information"
        data["value"] = self.request.user.id
        data["button"] = _("Send")
        return data

    def form_valid(self, form):
        new_address = form.save(commit=False)
        new_address.user_id = self.request.user.pk
        new_address.save()
        return super().form_valid(form)

    def get_success_url(self):
        address = Address.objects.get(user=self.request.user)
        return reverse_lazy("view-address", kwargs={"pk": address.pk})


class ViewAddressView(DetailView):
    template_name = "account/information/address.html"
    model = Address

    def get(self, request, *args, **kwargs):
        address = Address.objects.get(user_id=self.request.user.pk)
        if self.kwargs["pk"] != address.pk:
            return HttpResponseRedirect(
                reverse_lazy("view-address", kwargs={"pk": address.pk})
            )
        else:
            return super().get(request)


class EditAddressView(SuccessMessageMixin, UpdateView):
    template_name = "account/form.html"
    model = Address
    form_class = AddressForm
    success_message = _("Your new address has been registered.")

    def get(self, request, *args, **kwargs):
        address = Address.objects.get(user_id=self.request.user.pk)
        if self.kwargs["pk"] != address.pk:
            return HttpResponseRedirect(
                reverse_lazy("edit-address", kwargs={"pk": address.pk})
            )
        else:
            return super().get(request)

    def get_context_data(self, **kwargs):
        data = super(EditAddressView, self).get_context_data(**kwargs)
        data["title"] = _("Edit your address")
        data["link"] = "view-address"
        data["value"] = self.object.pk
        data["button"] = _("Edit")
        return data

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("view-address", kwargs={"pk": pk})


class ViewFavoriteView(ListView):
    template_name = "account/list.html"
    model = Favorite

    def get_context_data(self, **kwargs):
        data = super(ViewFavoriteView, self).get_context_data(**kwargs)
        data["title"] = _("Your favorites")
        data["message"] = _("You don't have any favorites yet.")
        data["view"] = "ad"
        data["delete"] = "delete-favorite"
        return data

    def get_queryset(self):
        return (
            Picture.objects.filter(product__favorite__user_id=self.request.user.pk)
            .all()
            .order_by("product__title")
        )


class DeleteFavoriteView(RedirectView):
    def get(self, request, *args, **kwargs):
        Favorite.objects.get(
            product_id=self.kwargs["pk"], user_id=self.request.user.pk
        ).delete()
        messages.success(request, _("The ad has been removed from your favorites."))
        return HttpResponseRedirect(reverse_lazy("list-favorites"))


class DeleteProfilView(DeleteView):
    success_url = reverse_lazy("index")
    template_name = "account/information/delete.html"
    model = User

    def get(self, request, *args, **kwargs):
        if self.request.user.pk == self.kwargs["pk"]:
            return super().get(request)
        else:
            return HttpResponseRedirect(
                reverse_lazy("profil-delete", kwargs={"pk": self.request.user.pk})
            )

    def delete(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _("Your account has been removed."))
        return super().delete(request)


class LogoutView(TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("index"))
