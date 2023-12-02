from celery import shared_task, current_task, task
from celery.result import AsyncResult
from time import sleep
from	.models	import	* 
import subprocess as sp
import logging
from celery import signals
import requests
import json
import urllib
from datetime import datetime
from django.db.models import Q
import os
import requests

logger = logging.getLogger('django')


@shared_task()
def loggs(message,type):
    if type== "error":
    	logger.error(message)
    elif type == "info":
        logger.info(meessage)


#@shared_task
#def semdSMS():
        #api.send_sms(body='Narayana', from_phone='xx', to=['+919618562678'])
        #account_sid = 'AC80ade6fc8817e3969cda6ef560de73f4'
        #auth_token = '56349b9caf8472fb0405512f180144fc'
        #client = Client(account_sid, auth_token)

        #message = client.messages.create(
        #                        body='Govinda',
        #                        from_='+12055498795',
        #                        to='+919618562678'
        #                        )
        #user = 'jayashankarbvr@gmail.com'
        #password = 'hARIgOVINDA@10'

        #voice = Voice()
        #voice.login(user, password)
        #util.pprint(voice.settings)

        
        #url = "https://www.fast2sms.com/dev/bulk"

        #payload = "sender_id=FSTSMS&message=This%20is%20a%20Hari%20Govinda&language=english&route=p&numbers=8106416598"
        #headers = {
        #'authorization': "mkGdSnvIl5F8XPDLTsqUWYpbAcwO2VJH3CM6oNBf9h7x10QugaAFeCzOEmcJXrUK8GHoBv2594bfNYqg",
        #'Content-Type': "application/x-www-form-urlencoded",
        #'Cache-Control': "no-cache",
        #}

        #response = requests.request("POST", url, data=payload, headers=headers)

        #print(response.text)

        #number = input('Number to send message to: ') # use these for command method
        #message = input('Message text: ')

        #voice.send_sms('+919618562678','Narayana')


@shared_task
def refreshDefects():
        error=""
        success=""
        srel_list=""
        wi1=[]
        repo	=	'https://jazz04.rchland.ibm.com:12443/jazz'
        aurl	=	repo+'/authenticated/identity'
        seccheck	=repo+'/j_security_check'

        rs=requests.Session()
        rs.get(aurl,allow_redirects=True, verify=False)

        authvalues	=	{
        'j_username':'bjayasan@in.ibm.com',
        'j_password':'GlobalIBM@)(*&^%$#@!'
                    }

        c=rs.post(seccheck,params=authvalues,allow_redirects=True, verify=False)

        authmsg	=	c.headers.get('X-com-ibm-team-repository-web-auth-msg','None')
        if	authmsg	==	"authfailed":
                error="Authorization	failed"
        else:
            count=0
            #r_uri="https://jazz04.rchland.ibm.com:12443/jazz/oslc/contexts/_95BkoA4_EeKDTutUyZ4Kbw/workitems?&oslc.paging=true&oslc.pageSize=100&oslc.select=dcterms:identifier,dcterms:title,oslc_cm:status,dcterms:type,rtc_cm:filedAgainst,oslc_cm:relatedTestCase,rtc_ext:com.ibm.stg.attribute.phaseFound,rtc_cm:plannedFor&oslc.where=rtc_cm:plannedFor%20in%20%5B"	+	srel_list	+	"%5D%20and%20rtc_cm:type=%22com.ibm.stg.workItemType.stgDefect%22&_startIndex="	+	str(count)
            #r_uri="https://jazz04.rchland.ibm.com:12443/jazz/oslc/contexts/_95BkoA4_EeKDTutUyZ4Kbw/workitems?&oslc.paging=true&oslc.pageSize=100&oslc.select=dcterms:identifier,dcterms:creator,dcterms:modified,dcterms:title,oslc_cm:status,dcterms:type,rtc_cm:filedAgainst,oslc_cm:relatedTestCase,rtc_ext:com.ibm.stg.attribute.phaseFound,rtc_cm:plannedFor,oslc_cmx:severity&oslc.where=rtc_cm:plannedFor%20in%20%5B"	+	srel_list	+	"%5D&_startIndex="	+	str(count)
            r_uri="https://jazz04.rchland.ibm.com:12443/jazz/oslc/contexts/_95BkoA4_EeKDTutUyZ4Kbw/workitems?&oslc.paging=true&oslc.pageSize=100&oslc.select=dcterms:identifier,oslc_cm:status,dcterms:created,dcterms:modified,dcterms:creator,rtc_cm:filedAgainst,rtc_cm:teamArea&oslc.where=rtc_cm:type=%22com.ibm.stg.workItemType.stgDefect%22%20and%20rtc_cm:foundIn=%22https://jazz04.rchland.ibm.com:12443/jazz/resource/itemOid/com.ibm.team.workitem.Deliverable/_dyUTkOEHEemFjoo4aH8nDw%22&_startIndex="+	str(count)
            headers={'Accept':'application/json'}
            headers['OSLC-Core-Version']='2.0'
            c=rs.get(r_uri,headers=headers,allow_redirects=True,verify=False)
            wi=json.loads(c.content)
            count=int(wi['oslc:responseInfo']['oslc:totalCount'])
            xx=count
                            
            count=0
                            
            while	(count	<=	xx):
                                                
                                                if 'oslc:results' in wi:
                                                                    wi1+=wi['oslc:results']
                                                count+=100
                                                #r_uri="https://jazz04.rchland.ibm.com:12443/jazz/oslc/contexts/_95BkoA4_EeKDTutUyZ4Kbw/workitems?&oslc.paging=true&oslc.pageSize=100&oslc.select=dcterms:identifier,dcterms:creator,dcterms:modified,dcterms:title,oslc_cm:status,dcterms:type,rtc_cm:filedAgainst,oslc_cm:relatedTestCase,rtc_ext:com.ibm.stg.attribute.phaseFound,rtc_cm:plannedFor,oslc_cmx:severity&oslc.where=rtc_cm:plannedFor%20in%20%5B"	+	srel_list	+	"%5D&_startIndex="	+	str(count)
                                                r_uri="https://jazz04.rchland.ibm.com:12443/jazz/oslc/contexts/_95BkoA4_EeKDTutUyZ4Kbw/workitems?&oslc.paging=true&oslc.pageSize=100&oslc.select=dcterms:identifier,oslc_cm:status,dcterms:created,dcterms:modified,dcterms:creator,rtc_cm:filedAgainst,rtc_cm:teamArea&oslc.where=rtc_cm:type=%22com.ibm.stg.workItemType.stgDefect%22%20and%20rtc_cm:foundIn=%22https://jazz04.rchland.ibm.com:12443/jazz/resource/itemOid/com.ibm.team.workitem.Deliverable/_dyUTkOEHEemFjoo4aH8nDw%22&_startIndex="+	str(count)

                                                c=rs.get(r_uri,headers=headers,allow_redirects=True,verify=False)
                                                wi=json.loads(c.content)
            for	x	in	wi1:
                                    #Filed	Against
                                    fa=""
                                    fa=(x['rtc_cm:filedAgainst']['rdf:resource']).split("/")
                                    fa=fa[len(fa)-1]
                                    #Creator
                                    cr=""
                                    cr=(x['dcterms:creator']['rdf:resource']).split("/")
                                    cr=cr[len(cr)-1]
                                    cr=urllib.parse.unquote(cr)
                                    cr=cr.split('@')[0]
                                    #cr=urllib.unquote(cr)
                                    #Created date
                                    y=x['dcterms:created'].split("T")
                                    y=y[0]
                                    #Modified Date
                                    z=x['dcterms:modified'].split("T")
                                    z=z[0]
                                    #TeamArea
                                    ta=""
                                    ta=(x['rtc_cm:teamArea']['rdf:resource']).split("/")
                                    ta=ta[len(ta)-1]
                                    try:
                                                defect = Defects.objects.get(pk=x['dcterms:identifier'])
                                                defect.status=x['oslc_cm:status']
                                                defect.modified_dt=z 
                                                defect.teamArea=ta
                                                defect.save()
                                    except	Defects.DoesNotExist:
                                                #import pdb; pdb.set_trace()																																
                                                defect=Defects( defect_id=x['dcterms:identifier'],
                                                            creator=cr,
                                                            status= str(x['oslc_cm:status']).strip(),
                                                            team_area=ta.strip(),
                                                            created_dt=datetime.strptime(y,"%Y-%m-%d").date(),
                                                            modified_dt=datetime.strptime(z,"%Y-%m-%d").date(),
                                                            filed_against=fa )
                                                defect.save()
