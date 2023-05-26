from django.urls import path
from .views import queries, query, uploadings,download,augmentators, augmentation
app_name = 'query'
urlpatterns = [
    path('', queries, name='index'),
    path('<int:pk>', query, name='query'),
    path('upl/', uploadings, name='uploadings'),
    path('aug/', augmentators, name='augmentations'),
    path('aug/<int:pk>', augmentation, name='augmentation'),
    path('download/<str:file_base_name>/', download, name='download')
]