
from django.urls import path
from . import views


urlpatterns=[

path('', views.login_user, name='login_user'),

path('list_main', views.list_main, name='list_main'),

path('logout', views.logout_user, name='logout_user'),

path('addhost',	views.add_host,	name='add_host'),

path('edithost',	views.edit_host,	name='edit_host'),

path('deletehost',	views.delete_host,	name='delete_host'),

path('exporthostlist',	views.export_host_list,	name='export_host_list'),

path('exporthmclist',	views.export_hmc_list,	name='export_hmc_list'),

path('exportstoragelist',	views.export_storage_list,	name='export_storage_list'),

path('exportfabriclist',	views.export_fabric_list,	name='export_fabric_list'),

path('addhmc',	views.add_hmc,	name='add_hmc'),

path('edithmc',	views.edit_hmc,	name='edit_hmc'),

path('deletehmc',	views.delete_hmc,	name='delete_hmc'),

path('addstorage',	views.add_storage,	name='add_storage'),

path('editstorage',	views.edit_storage,	name='edit_storage'),

path('deletestorage',	views.delete_storage,	name='delete_storage'),

path('addfabric',	views.add_fabric,	name='add_fabric'),

path('editfabric',	views.edit_fabric,	name='edit_fabric'),

path('deletefabric',	views.delete_fabric,	name='delete_fabric'),

path('addimage',	views.add_image,	name='add_image'),

path('editimage',	views.edit_image,	name='edit_image'),

path('deleteimage',	views.delete_image,	name='delete_image'),

path('addnetwork',	views.add_network,	name='add_network'),

path('editnetwork',	views.edit_network,	name='edit_network'),

path('editnetworknode',	views.edit_network_node,	name='edit_network_node'),

path('deletenetwork',	views.delete_network,	name='delete_network'),

path('deletenetworknode',	views.delete_network_node,	name='delete_network_node'),

path('addsupportlevel',	views.add_supported_level,	name='add_supported_level'),

path('editsupportlevel',	views.edit_supported_level,	name='edit_supported_level'),

path('deletesupportlevel',	views.delete_supported_level,	name='delete_supported_level'),

path('listsupportlevel',	views.list_supported_levels,	name='list_supported_levels'),

path('detail_list_supported_levels/<str:pvc_release>',	views.detail_list_supported_levels,	name='detail_list_supported_levels'),

path('listhosts',	views.list_hosts,	name='list_hosts'),

path('listhoststype',	views.list_hosts_type,	name='list_hosts_type'),

path('listhmcs',	views.list_hmcs,	name='list_hmcs'),

path('liststorages',	views.list_storages,	name='list_storages'),

path('listfabrics',	views.list_fabrics,	name='list_fabrics'),

path('listsquadwise',	views.list_squad_wise,	name='list_squad_wise'),

path('deletescheduler',	views.delete_scheduler,	name='delete_scheduler'),

path('listscheduler',	views.list_scheduler,	name='list_scheduler'),

path('listnetworks',	views.list_networks,	name='list_networks'),

path('listimages',	views.list_images,	name='list_images'),

path('snapshot',	views.snapshot,	name='snapshot'),

path('restore',	views.restore,	name='restore'),

path('emailnotify',	views.email_notify,	name='email_notify'),

path('hostgroups',	views.host_groups,	name='host_groups'),

path('deletehostgroups',	views.delete_host_groups,	name='delete_host_groups'),

path('hosttypes',	views.host_types,	name='host_types'),

path('deletehosttypes',	views.delete_host_types,	name='delete_host_types'),

path('squadupdate',	views.squad_update,	name='squad_update'),

path('squaddelete',	views.squad_delete,	name='squad_delete'),

path('importdata',	views.import_data,	name='import_data'),

path('listlogs',	views.list_logs,	name='list_logs'),

path('task_status/<int:task_id>',	views.task_status,	name='task_status'),






]


