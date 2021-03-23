from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView
from app.models import Categorie, Product, Picture


class IndexView(ListView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data["products"] = Picture.objects.all()[:8]
        return data

    def get_queryset(self):
        return Categorie.objects.all().order_by("name")


class SearchRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        search = self.request.POST["input-search"]
        if search == "":
            return reverse_lazy("search")
        else:
            return reverse_lazy("search-name", kwargs={"search": search})


class SearchAllView(ListView):
    template_name = "search.html"
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(SearchAllView, self).get_context_data(**kwargs)
        data["categories"] = Categorie.objects.all().order_by("name")
        return data

    def get_queryset(self):
        return Picture.objects.all()[:32]


class SearchView(ListView):
    template_name = "search.html"
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(SearchView, self).get_context_data(**kwargs)
        data["categories"] = Categorie.objects.all().order_by("name")
        data["search"] = self.kwargs["search"]
        return data

    def get_queryset(self):
        search = self.kwargs["search"]
        return Picture.objects.all().filter(
            Q(product__title__icontains=search)
            | Q(product__categorie__name__icontains=search)
        )[:32]


class SearchCategorieView(ListView):
    template_name = "search.html"
    model = Categorie

    def get_context_data(self, **kwargs):
        data = super(SearchCategorieView, self).get_context_data(**kwargs)
        data["categories"] = Categorie.objects.all().order_by("name")
        return data

    def get_queryset(self):
        return Picture.objects.filter(product__categorie_id=self.kwargs["pk"]).all()[
            :32
        ]
