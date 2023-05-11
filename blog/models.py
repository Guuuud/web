from django.db import models
from django.urls import reverse
# Create your models here.

class Airline(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('post_detail',args=[str(self.id)])



class PaymentService(models.Model):
    id = models.IntegerField(primary_key=True)

    url = models.URLField(max_length=500)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.url
