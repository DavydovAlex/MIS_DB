from django.contrib import admin
from . import models


class ParamsInline(admin.StackedInline):
    model = models.Params
    extra = 0
# Register your models here.
@admin.register(models.Query)
class QueryModelAdmin(admin.ModelAdmin):
    fields = ('name', 'query', 'description')
    list_display = ('name', 'description')
    inlines = [
        ParamsInline
    ]

