from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http.response import HttpResponseNotAllowed, HttpResponseBadRequest

from app_2012_majus_idegen.models import Extent, Naming, Restriction

# Create your views here.


def index(request):
    return render(request, "index.html")


def upload(request):
    return render(request, "upload.html")


def uploaded(request: HttpRequest):
    if request.method.lower() != "post":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    if not all(elem in request.FILES.keys() for elem in ["extent", "naming", "restriction"]):
        return HttpResponseBadRequest("Hiányzó fájlok")

    count, error = Extent.create_from_source(
        str(request.FILES["extent"].file.read(), encoding="utf-8"))
    if error:
        return HttpResponseBadRequest(f"{count} extent adatot sikerült létrehozni, de a következő hiba miatt nem sikerült a többit: {error}")

    count, error = Naming.create_from_source(
        str(request.FILES["naming"].file.read(), encoding="utf-8"))
    if error:
        return HttpResponseBadRequest(f"{count} naming adatot sikerült létrehozni, de a következő hiba miatt nem sikerült a többit: {error}")

    count, error = Restriction.create_from_source(
        str(request.FILES["restriction"].file.read(), encoding="utf-8"))
    if error:
        return HttpResponseBadRequest(f"{count} restriction adatot sikerült létrehozni, de a következő hiba miatt nem sikerült a többit: {error}")

    total = Restriction.objects.count() + Naming.objects.count() + Extent.objects.count()
    return HttpResponse(f"Az adatok sikeresen feltöltődtek. Összesen {total} adat van az adatbázisban.")

def _2miskolc(request: HttpRequest):
    context = {
        "restrictions": Restriction.objects.filter(settlement="Miskolc")
    }
    return render(request, "feladat/2miskolc.html", context)

def _3accordingtotime(request: HttpRequest):
    context = {
        "restrictions": sorted([{ "duration": (restriction.towhen - restriction.fromwhen).days, "settlement": restriction.settlement } for restriction in Restriction.objects.all()], key=lambda x: x["duration"], reverse=True)
    }
    return render(request, "feladat/3accordingtotime.html", context)

def _4junction(request: HttpRequest):
    context = {
        "settlements": set([restriction.settlement for restriction in Restriction.objects.all() if restriction.naming.name == "junction construction"])
    }
    return render(request, "feladat/4junction.html", context)

def _5four(request: HttpRequest):
    context = {
        "count": len([restriction for restriction in Restriction.objects.all() if len(str(restriction.roadnumber)) == 4])
    }
    return render(request, "feladat/5four.html", context)

def _6average(request: HttpRequest):
    context = {
        
    }
    return render(request, "feladat/6average.html", context)

def _7roadreport(request: HttpRequest):
    context = {

    }
    return render(request, "feladat/7roadreport.html", context)
