from time import sleep
from	.models	import	* 
import subprocess as sp
import datetime
from django.core.mail import send_mail
import	subprocess


def	scheduled_notify():
		schedules=Schedules.objects.all()
		
		for sc in schedules:
			msg=""
			status , result = subprocess.getstatusoutput("ping -c1 -w2 " + str(sc.ip_add).strip())
			if status == 0:
					if sc.status=="Up":
						msg="Resource with the IP << "+ sc.ip_add +" >> is UP"
			else:
					if sc.status=="Down":
						msg="Resource with the IP << "+ sc.ip_add +" >> is Down"

			if msg:
				
				if (sc.notify_date < datetime.date.today()) or ((sc.notify_date==datetime.date.today()) and (sc.notified_today==False)):
						subject = msg
						message = "Pls be informed that the " + msg
						to_email=[]
						to_email=str(sc.notify_id).split(',')
						X=0
						for n in to_email:
							to_email[X]=str(n).strip()
							X=X+1
						if subject and message	and	len(to_email):
										try:
														send_mail(subject, message, "",	to_email,	fail_silently=False )

														
										except :
													pass
										
										try:
												sc1=Schedules.objects.get(pk=str(sc.ip_add).strip())
												sc1.notify_date=datetime.date.today()
												sc1.notified_today=True
												sc1.save()
										
										except Schedules.DoesNotExist:	 
												pass


     

def refreshStatus():
    status = ""
    result = ""
    hosts = Hosts.objects.all()
    for host in hosts:
        status , result = sp.getstatusoutput("ping -c1 -w2 " + str(host.cec_fsp_bmc_ip))
        if status == 0:
            host.cec_ip_ping = True
        else:
            host.cec_ip_ping = False
        host.save()
    
    hmcs = Hmcs.objects.all()
    for hmc in hmcs:
        status , result = sp.getstatusoutput("ping -c1 -w2 " + str(hmc.hmc_public_ip))
        if status == 0:
            hmc.hmc_ip_ping=True
        else:
            hmc.hmc_ip_ping=False
        hmc.save()
    
    storages = Storages.objects.all()
    for storage in storages:
        status , result = sp.getstatusoutput("ping -c1 -w2 " + str(storage.storage_ip))
        if status == 0:
            storage.storage_ip_ping = True
        else:
            storage.storage_ip_ping = False
        storage.save()

    fabrics = Fabrics.objects.all()
    for fabric in fabrics:
        status , result = sp.getstatusoutput("ping -c1 -w2 " + str(fabric.fabric_ip))
        if status == 0:
            fabric.fabric_ip_ping = True
        else:
            fabric.fabric_ip_ping = False
        fabric.save()
    
    nwnodes = NetworkNodes.objects.all()
    for nwnode in nwnodes:
        status , result = sp.getstatusoutput("ping -c1 -w2 " + str(nwnode.network_node_ip))
        if status == 0:
            nwnode.network_node_ip_ping = True
        else:
            nwnode.network_node_ip_ping = False
        nwnode.save()