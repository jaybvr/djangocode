from django.db import models

# Create your models here.



class	Hosts(models.Model):
							cec_fsp_bmc_ip	= models.CharField(max_length=200,	primary_key=True)
							cec_ip_ping = models.BooleanField(default=False)
							cec_fsp_credentials	= models.CharField(max_length=200)
							cec_type	= models.CharField(max_length=200)
							cec_squad	= models.CharField(max_length=200,	default="POOL")
							cec_owner	= models.CharField(max_length=200)
							cec_name	= models.CharField(max_length=200)
							cec_serial	= models.CharField(max_length=200)
							cec_location	= models.CharField(max_length=200)
							cec_firmware	= models.CharField(max_length=200)
							cec_hmc_ip	= models.CharField(max_length=200)
							cec_neo_ip	= models.CharField(max_length=200)
							cec_vios1	= models.CharField(max_length=200)
							cec_vios2	= models.CharField(max_length=200)
							cec_proc_memory	= models.CharField(max_length=200)
							cec_model	= models.CharField(max_length=200)
							cec_network_ports	= models.CharField(max_length=200)
							cec_fabric1	= models.CharField(max_length=200)
							cec_fabric2	= models.CharField(max_length=200)
							cec_pvlan=models.CharField(max_length=200,	default="")
							cec_storages=models.CharField(max_length=1000,	default="")
							cec_lab	=	models.CharField(max_length=200)

class	Hmcs(models.Model):
								hmc_public_ip	=	models.CharField(max_length=200,	primary_key=True)
								hmc_ip_ping = models.BooleanField(default=False)
								hmc_credentials	=	models.CharField(max_length=200)
								hmc_squad	=	models.CharField(max_length=200,	default="POOL")
								hmc_owner	=	models.CharField(max_length=200)
								hmc_serial	=	models.CharField(max_length=200)
								hmc_location	=	models.CharField(max_length=200)
								hmc_private_ip	=	models.CharField(max_length=200)
								hmc_private_credentials	=	models.CharField(max_length=200)
								hmc_public_private	=	models.CharField(max_length=200)
								hmc_imm_ip	=	models.CharField(max_length=200)
								hmc_mtms	=	models.CharField(max_length=200)
								hmc_imm_credentials	=	models.CharField(max_length=200)
								hmclab	=	models.CharField(max_length=200)

class	Storages(models.Model):
								storage_ip	=	models.CharField(max_length=200,	primary_key=True)
								storage_ip_ping = models.BooleanField(default=False)
								storage_credentials	=	models.CharField(max_length=200)
								storage_type	=	models.CharField(max_length=200)
								storage_port	=	models.CharField(max_length=10,	default=0)
								storage_serial	=	models.CharField(max_length=200)
								storage_rest_api_server	=	models.CharField(max_length=200,	default=0)
								storage_ldev_id_range	=	models.CharField(max_length=200,	default=0)
								storage_location	=	models.CharField(max_length=200)
								storage_capacity	=	models.CharField(max_length=200)
								storage_service_ip	=	models.CharField(max_length=200)
								storage_lab	=	models.CharField(max_length=200)


class	Fabrics(models.Model):
								fabric_ip	=	models.CharField(max_length=200,	primary_key=True)
								fabric_ip_ping = models.BooleanField(default=False)
								fabric_credentials	=	models.CharField(max_length=200)
								fabric_type	=	models.CharField(max_length=200)
								fabric_primary	=	models.CharField(max_length=200)
								fabric_primary_port	=	models.CharField(max_length=10,	default=0)
								fabric_vsan_id	=	models.CharField(max_length=10,	default=0)
								fabric_serial	=	models.CharField(max_length=200)
								fabric_location	=	models.CharField(max_length=200)
								fabric_lab	=	models.CharField(max_length=200)
								fabric_storwise	=	models.CharField(max_length=1000)
								fabric_ds8k	=	models.CharField(max_length=1000)
								fabric_emc_vmax	=		models.CharField(max_length=1000)
								fabric_emc_vnx	=		models.CharField(max_length=1000)
								fabric_hitachi	=		models.CharField(max_length=1000)
								fabric_xiv	=	models.CharField(max_length=1000)


class	SupportedLevels(models.Model):
								pvc_release	=	models.CharField(max_length=20,	primary_key=True)
								sld=models.CharField(max_length=1000,default="")
								test_plan=models.CharField(max_length=1000,default="")
								management_node=models.CharField(max_length=1000,default="")
								hmc_level=models.CharField(max_length=1000,default="")
								vios_level=models.CharField(max_length=1000,default="")
								novalink_level=models.CharField(max_length=1000,default="")
								novalink_os=models.CharField(max_length=1000,default="")
								guest_os=models.CharField(max_length=1000,default="")
								storages=models.CharField(max_length=1000,default="")
								comments	=	models.TextField(default="")


class	Pvc_Images(models.Model):
									image_volume	=	models.CharField(max_length=200,	primary_key=True)
									owner	=	models.CharField(max_length=200)
									storage	=	models.CharField(max_length=200)
									operating_system	=	models.CharField(max_length=200)

class	Networks(models.Model):
								vlan_id	=	models.CharField(max_length=200,	primary_key=True)
								subnet_mask	=	models.CharField(max_length=200)
								gateway	=	models.CharField(max_length=200)
								dns1	=	models.CharField(max_length=200)
								dns2	=	models.CharField(max_length=200)


class	NetworkNodes(models.Model):
								network_node_ip	=	models.CharField(max_length=200,	primary_key=True)
								network_node_ip_ping = models.BooleanField(default=False)
								credentials	=	models.CharField(max_length=200)
								x_ppc	=	models.CharField(max_length=20)
								operating_system	=	models.CharField(max_length=200)


class	Snapshots(models.Model):
									timestamp=models.DateTimeField(auto_now=True,	primary_key=True)
									filepath=models.CharField(max_length=200)
									comments=models.TextField(default="")

			
class	HostGroups(models.Model):
								name=models.CharField(max_length=200,	primary_key=True)
								descreption=models.CharField(max_length=200)

class	HostTypes(models.Model):
								name=models.CharField(max_length=200,	primary_key=True)
								descreption=models.CharField(max_length=200)
								host_group=models.ForeignKey(HostGroups,	null=True,	on_delete=models.SET_NULL)
								
class	Squads(models.Model):
								name=models.CharField(max_length=200,	primary_key=True)
								descreption=models.CharField(max_length=200)
								
class Schedules(models.Model):
							ip_add = models.CharField(max_length=200, primary_key=True)
							timestamp = models.DateTimeField(auto_now=True)
							status = models.CharField(max_length=200)
							notify_date = models.DateField(auto_now=False)
							notified_today = models.BooleanField(default=False)
							notify_id = models.TextField(default="")
