from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from .models import Query, Params, Fields, ParamsValues, Uploadings
from django.db import transaction
from datetime import date, datetime
from django.core.paginator import Paginator
import os
from django.conf import settings


# Create your views here.

def queries(request):
    if request.method == "GET":
        queries = Query.objects.all().order_by('name')
        return render(request, 'queries.html', context={'queries': queries})
    elif request.method == 'POST':
        queries = Query.objects.filter(name__icontains=request.POST.get('filter')) | \
                  Query.objects.filter(description__icontains=request.POST.get('filter'))
        return render(request, 'queries.html', context={'queries': queries})


def query(request, pk):
    if request.method == "GET":
        query = Query.objects.get(pk=pk)
        query_params = query.get_params()
        query_fields = query.get_fields()
        context = {'query': query,
                   'params': query_params,
                   'fields': query_fields
                   }
        return render(request, 'query.html', context=context)
    elif request.method == 'POST':
        query = Query.objects.get(pk=pk)
        query_params_dict = {param.name: request.POST.get(param.name) for param in Params.objects.filter(query=pk)}
        query.create_uploading(request.POST.get("comment"),
                               query_params_dict)

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

        upl_list.append(uploading_context)
    return render(request, 'uploadings.html', context={'upls': upl_list})


def download(request, file_base_name):
    file_path = str(settings.BASE_DIR) + '/data/' + file_base_name
    print('----------------')
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force_download")
            response['Content-Disposition'] = 'inline; filename=' + file_path #os.path.basename(file_path)
            return response
    # If file is not exists
