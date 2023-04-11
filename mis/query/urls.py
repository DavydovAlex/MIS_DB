from django.urls import path
from .views import queries, query, uploadings
app_name = 'query'
urlpatterns = [
    path('', queries, name='index'),
    path('<int:pk>', query, name='query'),
    path('upl/', uploadings, name='uploadings')
]