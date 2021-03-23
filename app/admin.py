from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import (
    Countrie,
    Region,
    Citie,
    Categorie,
    Picture,
    Product,
    User,
    Address,
    State,
    Favorite,
)

admin.site.register(Countrie)
admin.site.register(Region)
admin.site.register(Citie)
admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Categorie)
admin.site.register(State)
admin.site.register(Product)
admin.site.register(Picture)
admin.site.register(Favorite)
