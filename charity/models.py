from django.db import models
from django.contrib.auth.models import User

TYPE = (
    (0, 'fundacja'),
    (1, 'organizacja pozarządowa'),
    (2, 'zbiórka lokalna'),
)



class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class Institution(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE, default=1)
    categories = models.ManyToManyField(Category)

    #class Meta:
    def __str__(self):
        return f"{self.name}"


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.PositiveIntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

