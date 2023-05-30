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
    fields = ('query','comment','status','create_date','file_path','uploaded_file')
    list_display = ('query','comment','status','create_date','file_path')

# @admin.register(models.Augmentations)
# class AugmentationsModelAdmin(admin.ModelAdmin):
#     fields = ('query', 'comment', 'status', 'create_date', 'file_path','uploaded_file')
#     list_display = ('query', 'comment', 'status', 'create_date', 'file_path','uploaded_file')

# @admin.register(models.UploadingFields)
# class AugmentationsModelAdmin(admin.ModelAdmin):
#     fields = ('augmentation', 'field')
#     list_display = ('augmentation', 'field')

@admin.register(models.ParamsValues)
class ParamsValuesModelAdmin(admin.ModelAdmin):
    fields = ('param', 'value','uploading')
    list_display = ('param', 'value','uploading')


@admin.register(models.Params)
class ParamsModelAdmin(admin.ModelAdmin):
    fields = ('name', 'type','description','query')
    list_display = ('name', 'type','description','query')