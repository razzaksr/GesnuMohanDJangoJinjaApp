from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from mongoengine import *
from certifi import *
from . import documents

myCert=where()
client=connect(host="mongodb+srv://razak:mohamed@cluster0.ptmlylq.mongodb.net/?retryWrites=true&w=majority",
               db="poc",username="razak",password="mohamed",tlsCAFile=myCert)
# Create your views here.

def makeCreate(req):
    eve=documents.Event()
    eve.initiate(input("Event name please "),datetime.fromisoformat(input("event date YYYY-MM-DD")),input("Event organising department "))
    #eve.initiate("Picconet11",datetime.fromisoformat("2022-12-20"),"CSE")
    eve.save()
    return HttpResponse('Event has added')

def makeList(req):
    mine=documents.Event.objects.all()
    for x in mine:print(x)
    return HttpResponse("Event has listed")