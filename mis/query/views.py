from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from .models import Query, Params, Fields ,ParamsValues, Uploadings
from django.db import transaction

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
            for field in query_fields:
                field.actual_name = field.actual_name if field.actual_name else field.default_name

        except Fields.DoesNotExist:
            query_fields = None
        context = {'query': query,
                   'params': query_params,
                   'fields': query_fields
                   }
        return render(request, 'query.html', context=context)
    elif request.method == 'POST':
        query_params = Params.objects.filter(query=pk)
        with transaction.atomic():
            p = Uploadings.objects.create(query=Query(id=pk), status=Uploadings.Status.IN_PROCESS, file_path='')
            for param in query_params:
                ParamsValues.objects.create(param=Params(param.id),value=request.POST.get(param.name),uploading=p)

        return HttpResponseRedirect(reverse('query:index'))


def uploadings(request):

    return render(request,'uploadings.html',context={})
