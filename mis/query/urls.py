from django.urls import path
from .views import queries,query
app_name = 'query'
urlpatterns = [
    path('', queries),
    path('<int:pk>',query, name='query')
]