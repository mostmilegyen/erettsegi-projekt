from django.db import models
import datetime

# Create your models here.

class Naming(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "naming"
        verbose_name_plural = "namings"

    def __str__(self):
        return self.name
    
    @staticmethod
    def create_from_source(text: str):
        text = text.strip()
        lines = [line.strip() for line in text.strip().split("\n")[1:]]

        count = 0
        for i,line in enumerate(lines):
            columns = line.split("\t")

            if len(columns) != 2:
                return count, f"Hiányzó adat(ok) vagy többletadat a(z) {i+1}. sorban."
            
            id, name = columns

            try:
                _, is_created = Naming.objects.get_or_create(
                    id=int(id),
                    name=name
                )
            except Exception:
                return count, f"Hibás formátumú adat(ok) a(z) {i+1}. sorban."

            if is_created:
                count += 1
            
        return count, None
    
class Extent(models.Model):
    
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "extent"
        verbose_name_plural = "extents"
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def create_from_source(text: str):
        text = text.strip()
        lines = [line.strip() for line in text.strip().split("\n")[1:]]

        count = 0
        for i,line in enumerate(lines):
            columns = line.split("\t")

            if len(columns) != 2:
                return count, f"Hiányzó adat(ok) vagy többletadat a(z) {i+1}. sorban."
            
            id, name = columns

            try:
                _, is_created = Extent.objects.get_or_create(
                    id=int(id),
                    name=name
                )
            except Exception:
                return count, f"Hibás formátumú adat(ok) a(z) {i+1}. sorban."

            if is_created:
                count += 1
            
        return count, None

class Restriction(models.Model):

    roadnumber = models.IntegerField()
    frompoint = models.FloatField()
    topoint = models.FloatField()
    settlement = models.CharField(max_length=50)

    fromwhen = models.DateField()
    towhen = models.DateField()
    naming = models.ForeignKey(Naming, on_delete=models.CASCADE)
    extent = models.ForeignKey(Extent, on_delete=models.CASCADE)
    speed = models.IntegerField(default=None, null=True)

    class Meta:
        verbose_name = "restriction"
        verbose_name_plural = "restrictions"

    def __str__(self):
        return f"Restriction: {self.roadnumber}, {self.settlement} {self.speed}km/h {self.fromwhen}-{self.towhen}"
    
    @staticmethod
    def create_from_source(text: str):
        text = text.strip()
        lines = [line.strip() for line in text.strip().split("\n")[1:]]

        count = 0
        for i,line in enumerate(lines):
            columns = line.split("\t")

            if len(columns) > 9 or len(columns) < 8:
                return count, f"Hiányzó adat(ok) vagy többletadat a(z) {i+1}. sorban."
            
            if len(columns) == 8:
                roadnumber, frompoint, topoint, settlement, fromwhen, towhen, namingid, extentid = columns
                speed = None
            else:
                roadnumber, frompoint, topoint, settlement, fromwhen, towhen, namingid, extentid, speed = columns

            naming = Naming.objects.filter(id=int(namingid)).first()
            if naming is None:
                return count, f"Még nem létezik a {i+1}. sorban szereplő naming."
            
            extent = Extent.objects.filter(id=int(extentid)).first()
            if extent is None:
                return count, f"Még nem létezik a {i+1}. sorban szereplő extent."

            try:
                _, is_created = Restriction.objects.get_or_create(
                    roadnumber=int(roadnumber),
                    frompoint=float(frompoint.replace(",", ".")),
                    topoint=float(topoint.replace(",", ".")),
                    settlement=settlement,
                    fromwhen=datetime.datetime.strptime(fromwhen, "%Y.%m.%d").date(),
                    towhen=datetime.datetime.strptime(towhen, "%Y.%m.%d").date(),
                    naming=naming,
                    extent=extent,
                    speed=int(speed) if speed is not None else None
                )
            except Exception as e:
                print(e)
                return count, f"Hibás formátumú adat(ok) a(z) {i+1}. sorban."

            if is_created:
                count += 1
            
        return count, None
    




