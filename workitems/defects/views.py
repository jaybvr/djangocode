from django.shortcuts import render
from .models import *
# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q

import requests
import json
import urllib

def index(request):
    return render(request,'defects/base_layout.html')



def	list_infra(request):
    d=""
    infraModifyDt=""
    infraVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    infraVerify=Defects.objects.filter(team_area='_9H83IHnLEeiLMo-WdXoaRQ',status='Verify').order_by('modified_dt')
    d=infraVerify.first()
    #import pdb; pdb.set_trace()
    #_9H83IHnLEeiLMo-WdXoaRQ
    if d:
            infraModifyDt=d.modified_dt
            clist=infraVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(infraVerify.filter(creator=x)))
                flist.append(temp)
    if len(flist)==1:
        flist.append([0,0])


    if infraModifyDt:
        infra_defects=Defects.objects.filter(Q(team_area='_9H83IHnLEeiLMo-WdXoaRQ'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=infraModifyDt))
        totalVerify=infraVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=infra_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=infraVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=infra_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_infra.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})

def list_interface(request):
    d=""
    interfaceModifyDt=""
    interfaceVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    interfaceVerify=Defects.objects.filter(team_area='_eFZO8HnUEeiLMo-WdXoaRQ',status='Verify').order_by('modified_dt')
    d=interfaceVerify.first()
    #import pdb; pdb.set_trace()

    if d:
            interfaceModifyDt=d.modified_dt
            clist=interfaceVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(interfaceVerify.filter(creator=x)))
                flist.append(temp)
    if len(flist)==1:
        flist.append([0,0])


    if interfaceModifyDt:
        interface_defects=Defects.objects.filter(Q(team_area='_eFZO8HnUEeiLMo-WdXoaRQ'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=interfaceModifyDt))
        totalVerify=interfaceVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=interface_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=interfaceVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=interface_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_interface.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})

def list_storage(request):
    d=""
    storageModifyDt=""
    storageVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    storageVerify=Defects.objects.filter(team_area='_voQfMHnIEeikntDAJzqVNA',status='Verify').order_by('modified_dt')
    d=storageVerify.first()
    #import pdb; pdb.set_trace()

    if d:
            storageModifyDt=d.modified_dt
            clist=storageVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(storageVerify.filter(creator=x)))
                flist.append(temp)
    if len(flist)==1:
         flist.append([0,0])


    if storageModifyDt:
        storage_defects=Defects.objects.filter(Q(team_area='_voQfMHnIEeikntDAJzqVNA'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=storageModifyDt))
        totalVerify=storageVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=storage_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=storageVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=storage_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_storage.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})

def list_framework(request):
    d=""
    frameworkModifyDt=""
    frameworkVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    frameworkVerify=Defects.objects.filter(team_area='_TocScHnVEeiLMo-WdXoaRQ',status='Verify').order_by('modified_dt')
    d=frameworkVerify.first()
    #import pdb; pdb.set_trace()

    if d:
            frameworkModifyDt=d.modified_dt
            clist=frameworkVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(frameworkVerify.filter(creator=x)))
                flist.append(temp)
    if len(flist)==1:
        flist.append([0,0])


    if frameworkModifyDt:
        framework_defects=Defects.objects.filter(Q(team_area='_TocScHnVEeiLMo-WdXoaRQ'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=frameworkModifyDt))
        totalVerify=frameworkVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=framework_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=frameworkVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=framework_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_framework.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})

def list_techm(request):
    d=""
    techmModifyDt=""
    techmVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    techmVerify=Defects.objects.filter(team_area='_LCFHgH7hEei_247Xkhp9Jg',status='Verify').order_by('modified_dt')
    d=techmVerify.first()
    #import pdb; pdb.set_trace()

    if d:
            techmModifyDt=d.modified_dt
            clist=techmVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(techmVerify.filter(creator=x)))
                flist.append(temp)

    if len(flist)==1:
        flist.append([0,0])


    if techmModifyDt:
        techm_defects=Defects.objects.filter(Q(team_area='_LCFHgH7hEei_247Xkhp9Jg'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=techmModifyDt))
        totalVerify=techmVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=techm_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=techmVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=techm_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_techm.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})

def list_novalink(request):
    d=""
    novalinkModifyDt=""
    novalinkVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    novalinkVerify=Defects.objects.filter(team_area='_RCKKADvjEem90uvezpzPKA',status='Verify').order_by('modified_dt')
    d=novalinkVerify.first()
    #import pdb; pdb.set_trace()

    if d:
            novalinkModifyDt=d.modified_dt
            clist=novalinkVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(novalinkVerify.filter(creator=x)))
                flist.append(temp)

    if len(flist)==1:
        flist.append([0,0])


    if novalinkModifyDt:
        novalink_defects=Defects.objects.filter(Q(team_area='_RCKKADvjEem90uvezpzPKA'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=novalinkModifyDt))
        totalVerify=novalinkVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=novalink_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=novalinkVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=novalink_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_novalink.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})


def	list_external(request):
    d=""
    extraModifyDt=""
    extraVerify=""
    totalVerify=""
    y=""
    pending=[]
    z={}
    clist=[]
    flist=[['Owner', 'Defect Count',]]

    extraVerify=Defects.objects.filter(team_area='_-C7HgA4_EeKDTutUyZ4Kbw',status='Verify').order_by('modified_dt')
    d=extraVerify.first()
    #import pdb; pdb.set_trace()
    #_9H83IHnLEeiLMo-WdXoaRQ
    if d:
            extraModifyDt=d.modified_dt
            clist=extraVerify.order_by('creator').values_list('creator',flat=True).distinct()
            for x in clist:
                temp=[]
                temp.append(x)
                temp.append(len(extraVerify.filter(creator=x)))
                flist.append(temp)
    if len(flist)==1:
        flist.append([0,0])


    if extraModifyDt:
        extra_defects=Defects.objects.filter(Q(team_area='_-C7HgA4_EeKDTutUyZ4Kbw'),Q(status='Verify')|Q(status='Closed'),Q(modified_dt__gte=extraModifyDt))
        totalVerify=extraVerify.values_list('defect_id',flat=True)
        for x in totalVerify:
            y+="  {  " + x + "  }  "
        #import pdb; pdb.set_trace()
        modify=extra_defects.order_by('-modified_dt').values_list('modified_dt',flat=True).distinct()

      
        for x in modify:
            z={}
            z['date']=x
            dl=""
            dayList=""
            dayList=extraVerify.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['verify']=dl
            dl=""
            dayList=""
            dayList=extra_defects.filter(Q(modified_dt=x)).values_list('defect_id',flat=True)
            for ver in dayList:
                dl+= "  {  " + ver + "  }  "
            z['closed']=dl

            pending.append(z)  

    return render(request,'defects/list_external.html',{'total':len(totalVerify),'tlist':y,'pending':pending,'flist':flist,'clist':clist})
