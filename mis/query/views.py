from django.shortcuts import render, HttpResponse
from .models import Query, Params, Fields

# Create your views here.

def queries(request):
    queries = Query.objects.all()
    return render(request,'queries.html',context={'queries':queries})


def query(request, pk):
    query = Query.objects.get(pk=pk)
    query_params = Params.objects.get(query=pk)
    query_fields = Fields.objects.get(query=pk).order_by('order')

    return HttpResponse(query_params.description)