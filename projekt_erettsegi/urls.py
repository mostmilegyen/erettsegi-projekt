from django.contrib import admin
from django.urls import include, path

# mivel több applikációt is tervezünk, az adott kezdetű url-eket továbbirányítjuk az applikáció urls.py-ába. Az amúgy magától nem volt ott, létre kellett hozni.

urlpatterns = [
    path('admin/', admin.site.urls),
    path("2012/majus/idegen/", include("app_2012_majus_idegen.urls"))
]
