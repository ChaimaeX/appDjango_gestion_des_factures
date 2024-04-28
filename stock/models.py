from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

# class Category(models.Model):
# 	name = models.CharField(max_length = 100)
# 	slug = models.SlugField(max_length = 150, unique=True ,db_index=True)
# 	icon = models.FileField(upload_to = "category/")
# 	create_at = models.DateTimeField(auto_now_add = True)
# 	updated_at = models.DateTimeField(auto_now_add = True)

# 	def __str__(self):
# 		return self.name
     
class Facture(models.Model):
    
     client = models.CharField(max_length=132)
     facture_date_time = models.DateTimeField(default=timezone.now)
     save_by = models.ForeignKey(User, on_delete=models.PROTECT )
     total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
     last_update_date = models.DateTimeField(null = True, blank=True)
     paid = models.BooleanField(default=False)
     # comments= models.TextField(null = True , max_length =1000, blank=True )

     class Meta:
          verbose_name = "Facture"
          verbose_name_plural ="Factures"

     def __str__(self):
         return f"{self.client}"
     @property
     def get_totals(self):
          produits = self.FactureProduct_set.all()
          total = sum(FactureProduct.produit.get_total for produit in produits)

class Devis(models.Model):
    
     client = models.CharField(max_length=132)
     Devis_date_time = models.DateField(auto_now_add=True)
     Description= models.TextField(null = True , max_length =1000, blank=True )
     save_by = models.ForeignKey(User , on_delete=models.PROTECT )
    


     class Meta:
          verbose_name = "Devis"
          verbose_name_plural ="Devis"

     def __str__(self):
         return f"{self.client} { self.Devis_date_time}"
     # @property
     # def get_totals(self):
     #      produits = self.Produit_set.all()
     #      total = sum(produit.get_total for produit in produits)     


class Chef(models.Model):
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    password = models.IntegerField()
    class Meta:
        verbose_name = "chef"

    def __str__(self):
          return self.name

class Produit(models.Model):
     """
     une facture associet a plusieur produit
     une produit associet a un facture
     # """
     
     # facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
     category =models.TextField(max_length=100)
     name = models.TextField(max_length=32)
     quantity = models.IntegerField()
     price = models.DecimalField(max_digits =100 , decimal_places=2)
     total = models.DecimalField(max_digits =100 , decimal_places=2)
     
     class Meta:
          verbose_name ="Produit"
          verbose_name_plural ="Produits"

     @property
     def get_total(self):
        total = self.quantity *self.price
     
class FactureProduct(models.Model):

     facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
     produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
     quantity_achat = models.IntegerField()
     price_finich = models.DecimalField(max_digits =100 , decimal_places=2)