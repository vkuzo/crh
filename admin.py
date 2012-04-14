from django.contrib import admin
from recycling.models import *

class RecyclerAdmin(admin.ModelAdmin):
	pass
	
class RecycleTypeAdmin(admin.ModelAdmin):
	pass

admin.site.register(Recycler, RecyclerAdmin)
admin.site.register(RecycleType, RecycleTypeAdmin)