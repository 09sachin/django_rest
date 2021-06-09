from django.contrib import admin
from .models import ToDo,TimeSeries,Dates,Delta7,Delta,Total,CRDTV
# Register your models here.

admin.site.register(ToDo)
admin.site.register(TimeSeries)
admin.site.register(Dates)
admin.site.register(Delta)
admin.site.register(Delta7)
admin.site.register(Total)
admin.site.register(CRDTV)
