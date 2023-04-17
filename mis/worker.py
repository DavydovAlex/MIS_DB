
import os
import sys

#sys.path.append('/app/mis/')
#from django import setup
import time
import threading
import asyncio
import django



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
    upl = Uploadings.objects.filter(pk=uploading.pk)
    usr = DbUsers.objects.filter(pk=user.pk)
    connection = database.DatabaseMis(user.login, user.password, dsn)
    param_values = ParamsValues.objects.filter(uploading=uploading.pk)
    upl.update(status=Uploadings.Status.IN_PROCESS)
    usr.update(in_process=True)
    select_query = query.Query(name=uploading.query.name, query=uploading.query.query, params={})
    data = connection.select(select_query)
    file_name = uploading.query.name + '_' + uploading.comment + '.xlsx'
    path = r'/app/data/' + file_name
    ex_w = filters.ExcelFilterWrite(path, chunk_size=999999, sheet_name='Sheet')
    handlers.ExcelHandler.write(data, ex_w)
    upl.update(file_path=path,status=Uploadings.Status.LOADED)
    usr.update(in_process=False)

if __name__ == "__main__":
    user = get_available_users()[0]
    upl = get_uploadings_to_process()[0]
    exec(user, upl)

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





