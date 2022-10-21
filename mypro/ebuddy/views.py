from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect
from mongoengine import *
from certifi import *
from . import documents

myCert=where()
client=connect(host="mongodb+srv://razak:mohamed@cluster0.ptmlylq.mongodb.net/?retryWrites=true&w=majority",
               db="poc",username="razak",password="mohamed",tlsCAFile=myCert)
# Create your views here.

def makeShort(req):
    if req.method=="POST":
        first=req.POST['dept']
        second=req.POST['date']
        if first=="Select Department":
            objs=documents.Event.objects(eveDate=second)
        else:
            objs=documents.Event.objects(eveDepartment=first)
        return render(req,'viewing.html',{"everything":objs})
    else:
        return render(req,'short.html')

def makeAnnounce(req,key,name):
    documents.Event.objects(eveId=key).update_one(set__eveWinner=name)
    return redirect("/buddy/")

def makeRemove(req,key,name):
    documents.Event.objects(eveId=key).update_one(pull__eveParticipants=name)
    return redirect("/buddy/")

def makeAddParts(req,pos):
    if req.method=="POST":
        eid=req.POST['eveid']
        part=req.POST['person']
        documents.Event.objects(eveId=eid).update_one(push__eveParticipants=part)
        return redirect('/buddy/')
    else:
        receive=documents.Event.objects(eveId=pos).first()
        return render(req,'enroll.html',{"ondru":receive})

def makeViewParts(req,key):
    receive=documents.Event.objects(eveId=key).first()
    return render(req,'people.html',{"all":receive})

def makeDelete(req,unique):
    receive=documents.Event.objects(eveId=unique).first()
    receive.delete()
    return redirect('/buddy/')

def makeEdit(req,num):
    if req.method=="POST":
        d=req.POST['eveid']
        nm=req.POST['evename']
        dt=req.POST['evedate']
        dp=req.POST['evedept']
        documents.Event.objects(eveId=d).update_one(set__eveName=nm,set__eveDate=dt,set__eveDepartment=dp)
        return redirect('/buddy/')
    else:
        receive=documents.Event.objects(eveId=num).first()
        return render(req,'edit.html',{"record":receive})

def makeRead(req,seriel):
    receive=documents.Event.objects(eveId=seriel).first()
    return render(req,'one.html',{"data":receive})

def makeCreate(req):
    if req.method=="POST":
        #print("POST accepted")
        nm=req.POST['evename']
        dt=req.POST['evedate']
        dp=req.POST['evedept']
        #print(nm,dt,dp)
        eve=documents.Event()
        eve.initiate(nm,datetime.fromisoformat(dt),dp)
        #eve.initiate("Picconet11",datetime.fromisoformat("2022-12-20"),"CSE")
        eve.save()
        return render(req,'schedule.html',{"info":nm+" has scheduled"})
    else:
        return render(req,'schedule.html')
    # eve=documents.Event()
    # eve.initiate(input("Event name please "),datetime.fromisoformat(input("event date YYYY-MM-DD")),input("Event organising department "))
    # #eve.initiate("Picconet11",datetime.fromisoformat("2022-12-20"),"CSE")
    # eve.save()
    # return HttpResponse('Event has added')

def makeList(req):
    mine=documents.Event.objects.all()
    # for x in mine:print(x)
    # return HttpResponse("Event has listed")
    return render(req,'viewing.html',{"everything":mine})

def makePage(req):
    return render(req,'begin.html')