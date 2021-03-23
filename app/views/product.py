from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    RedirectView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.utils.translation import gettext_lazy as _
from app.forms.product import AdForm, PictureForm, EditPictureForm
from app.models import Product, Picture, Address, Favorite


class NewAdView(CreateView):
    template_name = "account/form.html"
    model = Product
    form_class = AdForm

    def get(self, request, *args, **kwargs):
        if Address.objects.filter(user_id=self.request.user.pk).exists():
            return super().get(request)
        else:
            return HttpResponseRedirect(reverse_lazy("new-address"))

    def get_context_data(self, **kwargs):
        data = super(NewAdView, self).get_context_data(**kwargs)
        data["title"] = _("Add your ad")
        data["link"] = "index"
        data["button"] = _("Next")
        return data

    def form_valid(self, form):
        new_ad = form.save(commit=False)
        new_ad.user_id = self.request.user.pk
        new_ad.save()
        return super().form_valid(form)

    def get_success_url(self):
        product = Product.objects.filter(user_id=self.request.user.pk).latest("pk")
        return reverse_lazy("new-ad-picture", kwargs={"pk": product.pk})


class NewPictureView(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy("profil-ads")
    template_name = "account/form.html"
    model = Picture
    form_class = PictureForm
    success_message = _("Your ad has been published.")

    def get_context_data(self, **kwargs):
        data = super(NewPictureView, self).get_context_data(**kwargs)
        data["title"] = _("Add your pictures")
        data["back"] = "index"
        return data

    def form_valid(self, form):
        new_picture = form.save(commit=False)
        new_picture.product_id = self.kwargs["pk"]
        new_picture.save()
        return super().form_valid(form)


class ListAdView(ListView):
    template_name = "account/list.html"
    model = Product

    def get_context_data(self, **kwargs):
        data = super(ListAdView, self).get_context_data(**kwargs)
        data["title"] = _("Your ads")
        data["message"] = _("You have not yet published any ads.")
        data["view"] = "view-ad"
        data["edit"] = "edit-ad"
        data["delete"] = "delete-ad"
        return data

    def get_queryset(self):
        return Picture.objects.filter(product__user_id=self.request.user.pk).all()


class ViewAdView(DetailView):
    template_name = "product/ad.html"
    model = Product

    def get(self, request, *args, **kwargs):
        if Product.objects.filter(
            user_id=self.request.user.pk, id=self.kwargs["pk"]
        ).exists():
            return super().get(request)
        else:
            lastest = Product.objects.filter(user_id=self.request.user.pk).first()
            return HttpResponseRedirect(
                reverse_lazy("view-ad", kwargs={"pk": lastest.pk})
            )

    def get_context_data(self, **kwargs):
        data = super(ViewAdView, self).get_context_data(**kwargs)
        data["pictures"] = Picture.objects.filter(product_id=self.kwargs["pk"]).first()
        return data


class EditAdView(SuccessMessageMixin, UpdateView):
    template_name = "account/form.html"
    model = Product
    form_class = AdForm
    success_message = _("The ad has been modified.")

    def get(self, request, *args, **kwargs):
        if Product.objects.filter(
            user_id=self.request.user.pk, id=self.kwargs["pk"]
        ).exists():
            return super().get(request)
        else:
            lastest = Product.objects.filter(user_id=self.request.user.pk).first()
            return HttpResponseRedirect(
                reverse_lazy("edit-ad", kwargs={"pk": lastest.pk})
            )

    def get_context_data(self, **kwargs):
        data = super(EditAdView, self).get_context_data(**kwargs)
        data["pictures"] = Picture.objects.filter(product_id=self.kwargs["pk"]).first()
        data["extra"] = True
        data["title"] = _("Edit your ad")
        data["link"] = "profil-ads"
        data["button"] = _("Edit")
        return data

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("view-ad", kwargs={"pk": pk})


class EditPictureView(SuccessMessageMixin, UpdateView):
    template_name = "account/form.html"
    model = Picture
    form_class = EditPictureForm
    success_message = _("The image(s) have been modified.")

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(
            picture=self.kwargs["pk"], user_id=self.request.user.pk
        ).first()
        if Picture.objects.filter(product_id=product, id=self.kwargs["pk"]).exists():
            return super().get(request)
        else:
            product = Product.objects.filter(user_id=self.request.user.pk).first()
            lastest = Picture.objects.get(product_id=product)
            return HttpResponseRedirect(
                reverse_lazy("edit-ad-picture", kwargs={"pk": lastest.pk})
            )

    def get_context_data(self, **kwargs):
        data = super(EditPictureView, self).get_context_data(**kwargs)
        data["product"] = Product.objects.filter(picture=self.kwargs["pk"]).first()
        data["title"] = _("Edit your ad")
        data["link"] = "edit-ad"
        data["value"] = data["product"].id
        data["button"] = _("Edit")
        return data

    def get_success_url(self):
        product = Product.objects.get(picture=self.kwargs["pk"])
        return reverse_lazy("view-ad", kwargs={"pk": product.pk})


class DeleteAdView(DeleteView):
    success_url = reverse_lazy("profil-ads")
    template_name = "account/delete.html"
    model = Product

    def get(self, request, *args, **kwargs):
        if Product.objects.filter(
            user_id=self.request.user.pk, id=self.kwargs["pk"]
        ).exists():
            return super().get(request)
        else:
            lastest = Product.objects.filter(user_id=self.request.user.pk).first()
            return HttpResponseRedirect(
                reverse_lazy("delete-ad", kwargs={"pk": lastest.pk})
            )

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("The ad has been removed."))
        return super().delete(request)


class AdView(DetailView):
    template_name = "product/ad.html"
    model = Product

    def get_context_data(self, **kwargs):
        data = super(AdView, self).get_context_data(**kwargs)
        data["pictures"] = Picture.objects.filter(product_id=self.kwargs["pk"]).first()
        user_id = Product.objects.get(id=self.kwargs["pk"]).user.pk
        data["address"] = Address.objects.filter(user_id=user_id).first()
        data["products"] = (
            Picture.objects.filter(product__categorie_id=data["product"].categorie.id)
            .all()
            .exclude(product_id=self.kwargs["pk"])[:4]
        )
        if (
            not Picture.objects.filter(
                product__categorie_id=data["product"].categorie.id
            )
            .all()
            .exclude(product_id=self.kwargs["pk"])
            .exists()
        ):
            data["others"] = Picture.objects.all().exclude(
                product_id=self.kwargs["pk"]
            )[:4]
        data["favorite"] = Favorite.objects.filter(
            product_id=self.kwargs["pk"], user_id=self.request.user.pk
        ).exists()
        data["edit"] = Product.objects.filter(
            pk=self.kwargs["pk"], user_id=self.request.user.pk
        ).exists()
        return data


class OfferAdView(DetailView):
    template_name = "product/offer.html"
    model = Product

    def get_context_data(self, **kwargs):
        data = super(OfferAdView, self).get_context_data(**kwargs)
        user_id = Product.objects.get(id=self.kwargs["pk"]).user.pk
        data["address"] = Address.objects.filter(user_id=user_id).first()
        return data


class FavoriteView(RedirectView):
    def get(self, request, *args, **kwargs):
        if Favorite.objects.filter(
            product_id=self.kwargs["pk"], user_id=self.request.user.pk
        ).exists():
            Favorite.objects.get(
                product_id=self.kwargs["pk"], user_id=self.request.user.pk
            ).delete()
        else:
            Favorite.objects.create(
                product_id=self.kwargs["pk"], user_id=self.request.user.pk
            )
        return HttpResponseRedirect(
            reverse_lazy("ad", kwargs={"pk": self.kwargs["pk"]})
        )
