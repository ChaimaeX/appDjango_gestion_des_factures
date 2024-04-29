from django.contrib import admin
from .models import *
# Register your models here.

class Adminchef(admin.ModelAdmin):
    list_display = ('name' ,'email' , 'phone' ,'password')

class AdminFacture(admin.ModelAdmin):
    list_display= ('client','facture_date_time','save_by','paid')
    
admin.site.register(Chef,Adminchef)
admin.site.register(Facture,AdminFacture)
admin.site.register(Produit)
admin.site.register(FactureProduct)