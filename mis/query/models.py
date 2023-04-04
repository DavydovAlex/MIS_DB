from django.db import models

# Create your models here.
class Query(models.Model):
    name = models.CharField(max_length=100)
    query = models.TextField()
    description = models.CharField(max_length=200)

class Params(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)