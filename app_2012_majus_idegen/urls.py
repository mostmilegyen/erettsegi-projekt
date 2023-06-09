from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("upload/", views.upload),
    path("upload/uploaded/", views.uploaded),
    path("feladat/2miskolc", views._2miskolc),
    path("feladat/3accordingtotime", views._3accordingtotime),
    path("feladat/4junction", views._4junction),
    path("feladat/5four", views._5four),
    path("feladat/6average", views._6average),
    path("feladat/7roadreport", views._7roadreport)
]
