from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from .models import Query, Params, Fields

# Create your views here.

def queries(request):
    queries = Query.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


def query(request, pk):
    if request.method == "GET":
        query = Query.objects.get(pk=pk)
        query_params = Params.objects.filter(query=pk)
        try:
            query_fields = Fields.objects.filter(query=pk).order_by('order')
        except Fields.DoesNotExist:
            query_fields = None
        context = {'query': query,
                   'params': query_params,
                   'fields': query_fields
                   }
        return render(request, 'query.html', context=context)
    else:
        return HttpResponseRedirect(reverse('queries'))