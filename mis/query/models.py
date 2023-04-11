from django.db import models

# Create your models here.
class Query(models.Model):
    name = models.CharField(max_length=100, help_text='Введите имя запроса')
    query = models.TextField(help_text='Тело запроса')
    description = models.CharField(max_length=200, help_text='Краткое описание')

    def __str__(self):
        return self.description


class Params(models.Model):
    class Types(models.IntegerChoices):
        STR = 1
        INT = 2
        DATE = 3

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=Types.choices)
    description = models.CharField(max_length=200)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

class Fields(models.Model):
    order = models.IntegerField()
    default_name = models.CharField(max_length=100)
    actual_name = models.CharField(max_length=100, blank=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)



class Uploadings(models.Model):
    class Status(models.IntegerChoices):
        LOADED = 1
        IN_PROCESS = 2
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    file_path = models.FilePathField() #null=True, blank=True
    status = models.IntegerField(choices=Status.choices, default=Status.IN_PROCESS)


class ParamsValues(models.Model):
    param = models.ForeignKey(Params, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)
    uploading = models.ForeignKey(Uploadings, on_delete=models.CASCADE)



