"""LeBonRecoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from app.views.account import (
    RegisterView,
    LoginView,
    ProfilView,
    LogoutView,
    ViewInformationView,
    EditInformationView,
    NewAddressView,
    ViewAddressView,
    EditAddressView,
    ViewFavoriteView,
    DeleteFavoriteView,
    DeleteProfilView,
)
from app.views.error import (
    Custom400View,
    Custom403View,
    Custom404View,
)
from app.views.master import (
    IndexView,
    SearchRedirectView,
    SearchCategorieView,
    SearchView,
    SearchAllView,
)
from app.views.product import (
    ListAdView,
    ViewAdView,
    NewAdView,
    EditAdView,
    DeleteAdView,
    AdView,
    NewPictureView,
    EditPictureView,
    OfferAdView,
    FavoriteView,
)

admin.autodiscover()

urlpatterns = [path("admin/", admin.site.urls)]

urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", IndexView.as_view(), name="index"),
    path(_("register/"), RegisterView.as_view(), name="register"),
    path(_("login/"), LoginView.as_view(), name="login"),
    path(_("logout/"), LogoutView.as_view(), name="logout"),
    path(
        _("profil/"),
        login_required(ProfilView.as_view(), login_url=reverse_lazy("login")),
        name="profil",
    ),
    path(
        _("profil/delete/<int:pk>"),
        login_required(DeleteProfilView.as_view(), login_url=reverse_lazy("login")),
        name="profil-delete",
    ),
    path(
        _("profil/favorites"),
        login_required(ViewFavoriteView.as_view(), login_url=reverse_lazy("login")),
        name="list-favorites",
    ),
    path(
        _("profil/favorites/<int:pk>"),
        login_required(DeleteFavoriteView.as_view(), login_url=reverse_lazy("login")),
        name="delete-favorite",
    ),
    path(
        _("profil/information/<int:pk>"),
        login_required(ViewInformationView.as_view(), login_url=reverse_lazy("login")),
        name="view-information",
    ),
    path(
        _("profil/information/<int:pk>/edit"),
        login_required(EditInformationView.as_view(), login_url=reverse_lazy("login")),
        name="edit-information",
    ),
    path(
        _("profil/information/address"),
        login_required(NewAddressView.as_view(), login_url=reverse_lazy("login")),
        name="new-address",
    ),
    path(
        _("profil/information/address/<int:pk>"),
        login_required(ViewAddressView.as_view(), login_url=reverse_lazy("login")),
        name="view-address",
    ),
    path(
        _("profil/information/address/<int:pk>/edit"),
        login_required(EditAddressView.as_view(), login_url=reverse_lazy("login")),
        name="edit-address",
    ),
    path(
        _("profil/ads"),
        login_required(ListAdView.as_view(), login_url=reverse_lazy("login")),
        name="profil-ads",
    ),
    path(
        _("profil/ad/<int:pk>"),
        login_required(ViewAdView.as_view(), login_url=reverse_lazy("login")),
        name="view-ad",
    ),
    path(
        _("profil/ad/<int:pk>/edit"),
        login_required(EditAdView.as_view(), login_url=reverse_lazy("login")),
        name="edit-ad",
    ),
    path(
        _("profil/ad/picture/<int:pk>"),
        login_required(EditPictureView.as_view(), login_url=reverse_lazy("login")),
        name="edit-ad-picture",
    ),
    path(
        _("profil/ad/<int:pk>/delete"),
        login_required(DeleteAdView.as_view(), login_url=reverse_lazy("login")),
        name="delete-ad",
    ),
    path(_("ad/<int:pk>"), AdView.as_view(), name="ad"),
    path(
        _("ad/<int:pk>/offer"),
        login_required(OfferAdView.as_view(), login_url=reverse_lazy("login")),
        name="offer",
    ),
    path(
        _("ad/new"),
        login_required(NewAdView.as_view(), login_url=reverse_lazy("login")),
        name="new-ad",
    ),
    path(
        _("ad/new/<int:pk>"),
        login_required(NewPictureView.as_view(), login_url=reverse_lazy("login")),
        name="new-ad-picture",
    ),
    path(_("searching/"), SearchRedirectView.as_view(), name="searching"),
    path(_("search/"), SearchAllView.as_view(), name="search"),
    path(_("search/<str:search>"), SearchView.as_view(), name="search-name"),
    path(
        _("search/categorie/<int:pk>"),
        SearchCategorieView.as_view(),
        name="search-categorie",
    ),
    path(
        _("fav/<int:pk>"),
        login_required(FavoriteView.as_view(), login_url=reverse_lazy("login")),
        name="fav",
    ),
)

urlpatterns += static(settings.UPLOAD_FOLDER, document_root=settings.UPLOAD_ROOT)

handler400 = Custom400View.as_view()
handler403 = Custom403View.as_view()
handler404 = Custom404View.as_view()
