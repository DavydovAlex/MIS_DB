
import os
import sys

#sys.path.append('/app/mis/')
#from django import setup
import time
import threading
import django



django.setup()
from query.models import Uploadings,DbUsers
from ..DB import database

def get_available_users():
    return DbUsers.objects.filter(dont_use=False) & DbUsers.objects.filter(in_process=False)

def get_uploadings_to_process():
    return Uploadings.objects.filter(status=Uploadings.Status.WAITING).order_by('create_date')

if __name__ == "__main__":

    #while True:
        #time.sleep(100)
    users = get_available_users()
    uploadings = get_uploadings_to_process()
    print(uploadings[0].query.query)

    for upl in uploadings:
        users = get_available_users()
            #if users:





