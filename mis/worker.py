
import os
import sys

#sys.path.append('/app/mis/')
#from django import setup
import time
import threading
import asyncio
import django
from django.db import transaction
from django.conf import settings



django.setup()
from query.models import Uploadings,DbUsers,ParamsValues
from DB import database, query
from FileHandler import filters, handlers

def get_available_users():
    return DbUsers.objects.filter(dont_use=False) & DbUsers.objects.filter(in_process=False)

def get_uploadings_to_process():
    return Uploadings.objects.filter(status=Uploadings.Status.WAITING).order_by('create_date')

def exec(user, uploading):
    dsn = """
        (DESCRIPTION =
        (ADDRESS_LIST =
          (ADDRESS = (PROTOCOL = TCP)(HOST = 10.101.39.53)(PORT = 1521))
        )
        (CONNECT_DATA =
          (SERVICE_NAME = nsocluster)
    	  (SERVER = DEDICATED)
        )
      )
        """
    upl = Uploadings.objects.get(pk=uploading.pk)
    usr = DbUsers.objects.get(pk=user.pk)
    connection = database.DatabaseMis(user.login, user.password, dsn)
    params = upl.get_params_values()
    upl.status = Uploadings.Status.IN_PROCESS
    usr.in_process = True
    with transaction.atomic():
        upl.save()
        usr.save()
    try:
        select_query = query.Query(name=uploading.query.name,
                                   query=uploading.query.query,
                                   params=params)
        data = connection.select(select_query)
        print(data.columns)
        data.columns = uploading.query.get_actual_names()
        print(data.columns)
        file_name = uploading.query.name + '_' + str(int(time.time())) + '.xlsx'
        file_path = str(settings.BASE_DIR) + '/data/' + file_name
        print(data.head())

        ex_w = filters.ExcelFilterWrite(file_path, chunk_size=999999, sheet_name='Sheet')
        handlers.ExcelHandler.write(data, ex_w)
        upl.file_path = file_name
        upl.status = Uploadings.Status.LOADED
        upl.save()
    except Exception as e:
        print(e)
        upl.status = Uploadings.Status.WAITING
        usr.in_process = False
        with transaction.atomic():
            upl.save()
            usr.save()
    finally:
        usr.in_process = False
        usr.save()




if __name__ == "__main__":
    user = get_available_users()
    upl = get_uploadings_to_process()
    if user and upl:
        exec(user[0], upl[0])

    #while True:
        #time.sleep(100)
    # query =query.Query(name='tst',query='Select * from D_AGENTS where rownum<=100',params={})
    #
    # db = database.DatabaseMis('amdavidov_db', 'p123', dsn)
    # data = db.select(query)
    # print(data)

    # users = get_available_users()
    # uploadings = get_uploadings_to_process()
    # print(uploadings[0].query.query)
    #
    # for upl in uploadings:
    #     users = get_available_users()
            #if users:





