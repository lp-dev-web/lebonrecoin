from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class Custom400View(TemplateView):
    template_name = "error.html"

    def get_context_data(self, **kwargs):
        data = super(Custom400View, self).get_context_data(**kwargs)
        data["title"] = _("Error 400")
        data["message"] = _("The syntax of the query is incorrect.")
        return data


class Custom403View(TemplateView):
    template_name = "error.html"

    def get_context_data(self, **kwargs):
        data = super(Custom403View, self).get_context_data(**kwargs)
        data["title"] = _("Error 403")
        data["message"] = _("You do not have permission to access this resource.")
        return data


class Custom404View(TemplateView):
    template_name = "error.html"

    def get_context_data(self, **kwargs):
        data = super(Custom404View, self).get_context_data(**kwargs)
        data["title"] = _("Error 404")
        data["message"] = _("The page you are looking for cannot be found.")
        return data
