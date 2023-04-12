from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from .models import Query, Params, Fields ,ParamsValues, Uploadings
from django.db import transaction
from datetime import date,datetime
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

            p = Uploadings.objects.create(query=Query(id=pk), status=Uploadings.Status.IN_PROCESS,
                                          file_path='',comment=request.POST.get("comment"),create_date=datetime.now())
            for param in query_params:
                ParamsValues.objects.create(param=Params(param.id), value=request.POST.get(param.name), uploading=p)

        return HttpResponseRedirect(reverse('query:index'))


def uploadings(request):
    uploadings = Uploadings.objects.all().order_by('-create_date')
    upl_list = []

    for upl in uploadings:
        print(upl.pk)
        uploading_context = {
            'upl': upl,
            'query': Query.objects.get(pk=upl.query.pk),
            'params': ParamsValues.objects.filter(uploading=upl.pk)
        }
        print(ParamsValues.objects.filter(uploading=upl.pk).select_related('param').values())


        upl_list.append(uploading_context)
    return render(request,'uploadings.html',context={'upls': upl_list})
