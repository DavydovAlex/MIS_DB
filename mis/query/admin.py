from django.contrib import admin
from . import models


class ParamsInline(admin.StackedInline):
    model = models.Params
    extra = 0

class FieldsInline(admin.StackedInline):
    model = models.Fields
    extra = 0
# Register your models here.
@admin.register(models.Query)
class QueryModelAdmin(admin.ModelAdmin):
    fields = ('name', 'query', 'description', 'type')
    list_display = ('name', 'description', 'type')
    inlines = [
        ParamsInline,
        FieldsInline
    ]

@admin.register(models.DbUsers)
class DbUsersModelAdmin(admin.ModelAdmin):
    fields = ('login', 'password', 'dont_use', 'in_process')
    list_display = ('login',  'dont_use', 'in_process')

@admin.register(models.Uploadings)
class UploadingsModelAdmin(admin.ModelAdmin):
    fields = ('query','comment','status','create_date','file_path')
    list_display = ('query','comment','status','create_date','file_path')