from django.contrib import admin
from .models import *

admin.site.register(Hosts)
admin.site.register(Storages)
admin.site.register(Fabrics)
admin.site.register(Pvc_Images)
admin.site.register(SupportedLevels)
admin.site.register(Hmcs)
admin.site.register(Networks)
admin.site.register(NetworkNodes)
admin.site.register(HostGroups)
admin.site.register(HostTypes)
admin.site.register(Snapshots)


# Register your models here.
