from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from .models import Query, Params, Fields, ParamsValues, Uploadings
from django.db import transaction
from datetime import date, datetime
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.conf import settings
import time
from pathlib import Path


# Create your views here.

def queries(request):
    if request.method == "GET":
        queries = Query.get_queries_by_type(Query.Types.UPLOADING).order_by('name')
        return render(request, 'queries.html', context={'queries': queries})
    elif request.method == 'POST':
        queries = Query.objects.filter(Q(name__icontains=request.POST.get('filter')) |
                                       Q(description__icontains=request.POST.get('filter')),
                                       type=Query.Types.UPLOADING)
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

def handle_uploaded_file(f, file_name):
    print(settings.FILES_DIR / file_name)
    with open(settings.FILES_DIR / file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def augmentation(request, pk):
    if request.method == "GET":
        query = Query.objects.get(pk=pk)
        query_params = query.get_params()
        query_fields = query.get_fields()
        context = {'query': query,
                   'params': query_params,
                   'fields': query_fields
                   }
        return render(request, 'augmentation.html', context=context)
    elif request.method == 'POST':
        query = Query.objects.get(pk=pk)
        fileds = request.POST.getlist('fields')
        file = request.FILES['docpicker']
        _, file_extension = os.path.splitext(file.name)
        file_name = str(int(time.time())) + file_extension
        handle_uploaded_file(request.FILES['docpicker'], file_name)
        query_params_dict = {param.name: request.POST.get(param.name) for param in Params.objects.filter(query=pk)}
        query.create_augmentation_query(request.POST.get("comment"),
                                        file_name,
                                        fileds,
                                        query_params_dict)
        return HttpResponseRedirect(reverse('query:index'))


def uploadings(request):
    uploadings = Uploadings.objects.all().order_by('-create_date')
    upl_list = []

    for upl in uploadings:
        uploading_context = {
            'upl': upl,
            'query': Query.objects.get(pk=upl.query.pk),
            'params': ParamsValues.objects.filter(uploading=upl.pk)
        }

        upl_list.append(uploading_context)
    return render(request, 'uploadings.html', context={'upls': upl_list})

def augmentators(request):
    if request.method == "GET":
        queries = Query.get_queries_by_type(Query.Types.AUGMENTATION).order_by('name')
        return render(request, 'augmentations.html', context={'queries': queries})
    elif request.method == 'POST':
        queries = Query.objects.filter(Q(name__icontains=request.POST.get('filter')) |
                                       Q(description__icontains=request.POST.get('filter')),
                                       type=Query.Types.AUGMENTATION)
        return render(request, 'augmentations.html', context={'queries': queries})


def download(request, file_base_name):
    file_path = settings.FILES_DIR / file_base_name
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force_download")
            response['Content-Disposition'] = 'inline; filename=' + file_base_name #os.path.basename(file_path)
            return response
    # If file is not exists
