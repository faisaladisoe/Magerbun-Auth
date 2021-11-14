from django.db import models


# Create your models here.
class Menu(models.Model):
    makanan = "makanan"
    minuman = "minuman"
    list_category = [
        (makanan, "Makanan"),
        (minuman, "Minuman")
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    stock = models.PositiveIntegerField()
    description = models.TextField(max_length=250, default="deskripsi")
    category = models.CharField(choices=list_category, default=makanan, max_length=100)
