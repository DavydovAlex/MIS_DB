
from django.db import models, transaction
import datetime


# Create your models here.


class Query(models.Model):
    name = models.CharField(max_length=100, help_text='Введите имя запроса')
    query = models.TextField(help_text='Тело запроса')
    description = models.CharField(max_length=200, help_text='Краткое описание')

    def __str__(self):
        return self.description


    #TODO Add exception processing
    @transaction.atomic
    def create_uploading(self, comment, params):
        uploading = Uploadings.objects.create(query=Query(id=self.pk),
                                              status=Uploadings.Status.WAITING,
                                              file_path='',
                                              comment=comment,
                                              create_date=datetime.datetime.now())
        for param in Params.objects.filter(query=self.pk):
            ParamsValues.objects.create(param=Params(param.id),
                                        value=params[param.name],
                                        uploading=uploading)

    def get_fields(self):
        query_fields = Fields.objects.filter(query=self.pk).order_by('order')
        if query_fields:
            for field in query_fields:
                field.actual_name = field.actual_name if field.actual_name else field.default_name
            return query_fields
        else:
            raise self.NotDefinedFields('Query {0} has not defined fields'.format(self.name))

    def get_actual_names(self):
        fields = self.get_fields()
        names = []
        for field in fields:
            names.append(field.actual_name)
        return names

    def get_params(self):
        return Params.objects.filter(query=self.pk)

    class NotDefinedFields(Exception):
        """ Raised when not defined fields for query """
        pass






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

    def save(self, *args, **kwargs):
        self.actual_name = self.actual_name if self.actual_name else self.default_name
        super(Fields, self).save(*args, **kwargs)


class Uploadings(models.Model):
    class Status(models.IntegerChoices):
        WAITING = 0
        LOADED = 1
        IN_PROCESS = 2

    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    file_path = models.CharField(default='')  # null=True, blank=True
    status = models.IntegerField(choices=Status.choices, default=Status.WAITING)
    create_date = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    comment = models.CharField(max_length=200, blank=True)

    # def __str__(self):
    #     return '{}'.format()

    def get_params_values(self):
        params = {param.param.name: param.value for param in ParamsValues.objects.filter(uploading=self.id)}
        return params


class ParamsValues(models.Model):
    param = models.ForeignKey(Params, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)
    uploading = models.ForeignKey(Uploadings, on_delete=models.CASCADE)


class DbUsers(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dont_use = models.BooleanField(default=True)
    in_process = models.BooleanField(default=False)
