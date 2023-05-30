import datetime
import os
import sys
import traceback

# sys.path.append('/app/mis/')
# from django import setup
import time
import threading
import asyncio
import django
from django.db import transaction
from django.conf import settings

django.setup()
from query.models import Uploadings, DbUsers, ParamsValues, Query
# from DB import database, query
# from FileHandler import filters, handlers

from DB import database_new as database
from FileHandler import ExcelHandler


def get_available_users():
    return DbUsers.objects.filter(dont_use=False) & DbUsers.objects.filter(in_process=False)


def get_uploadings_to_process():
    return Uploadings.objects.filter(status=Uploadings.Status.WAITING).order_by('create_date')

def date_to_string(row):
    lst = list(row)
    for i, el in enumerate(lst):
        if isinstance(el, datetime.datetime):
            lst[i] = el.strftime('%d.%m.%Y')
    return lst


def augmentate():
    pass


def upload():
    pass


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
    connection = database.Oracle(user.login, user.password, dsn)
    upl.status = Uploadings.Status.IN_PROCESS
    usr.in_process = True
    with transaction.atomic():
        upl.save()
        usr.save()
    try:
        file_name = uploading.query.name + '_' + str(int(time.time())) + '.xlsx'
        file_path = str(settings.BASE_DIR) + '/data/' + file_name
        print(upl.query.type)
        if upl.query.type == Query.Types.UPLOADING:
            params = upl.get_params_values()
            select_query = database.Query(statement=uploading.query.query,
                                          params=params)
            cursor = connection.execute(select_query)
            cursor.header = uploading.query.get_actual_names()

            ex_h = ExcelHandler.ExcelHandler(file_path)
            ex_h.write(cursor)
            upl.file_path = file_name
            upl.status = Uploadings.Status.LOADED
            upl.save()
        else:
            fields = upl.get_uploading_fields()
            params = upl.get_params_values()
            ex_h = ExcelHandler.ExcelHandler(str(settings.BASE_DIR) + '/data/' + upl.uploaded_file)
            data_it = ex_h.get_data(2)
            for row in data_it:
                # print(row)
                print(params)
                date_to_string(row)
                row_params = {}
                for param in params:
                    if int(params[param]) != 0:
                        row_params[param] = date_to_string(row)[int(params[param])-1]
                    else:
                        row_params[param] = ''
                print(row_params)
                select_query = database.Query(statement=uploading.query.query, params=row_params)
                cursor = connection.execute(select_query)
                data = cursor.__next__()


    except Exception as e:
        print(e)
        print(''.join(traceback.TracebackException.from_exception(e).format()))
        upl.status = Uploadings.Status.WAITING
        usr.in_process = False
        with transaction.atomic():
            upl.save()
            usr.save()
    finally:
        usr.in_process = False
        usr.save()
        connection.close_connection()


if __name__ == "__main__":
    user = get_available_users()
    upl = get_uploadings_to_process()
    if user and upl:
        exec(user[0], upl[0])

    # while True:
    # time.sleep(100)
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
    # if users:
