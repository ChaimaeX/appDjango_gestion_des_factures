from django.shortcuts import render
from django.views import View
from .models import*
from django.contrib import messages
from django.db import transaction
from django.core.paginator import  (Paginator,EmptyPage)
from django.http import HttpResponse
import pdfkit
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


# pdfkit.from_url('http://google.com', 'out.pdf')
# pdfkit.from_file('test.html', 'out.pdf')
# pdfkit.from_string('Hello!', 'out.pdf') 

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.template.loader import get_template

from django.db import transaction

from .utils import pagination, get_facture

# from .decorators import *

from django.utils.translation import gettext as _
# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Chef

class LoginView(View):
    template_name = 'html/log_in.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
       try: 
          username = request.POST.get('username')
          password = request.POST.get('password')
          chef = Chef.objects.filter(name=username, password=password).first()
          if chef is not None:
              self.template_name = "html/index.html"
              return redirect('Home') 
          else:
              messages.warning(request, 'Username or password incorrect')
              return render(request, self.template_name)
       except Exception as e:
           messages.ERROR(request,'{e}')
           

class HomeView(View):
    templates_name='html/index.html'
    factures = Facture.objects.all().order_by('-facture_date_time')

    context={
        'factures': factures
    }
    def get(self, request, *args, **kwags):

        items = pagination(request, self.factures)

        self.context['factures'] = items

        return render(request, self.templates_name, self.context)

    def post(self,request,*args,**kwargs):
         
         #modifier un facture
         if request.POST.get('id_modified'):

            paid = request.POST.get('modified')

            try: 

                obj = Facture.objects.get(id=request.POST.get('id_modified'))

                if paid == 'True':

                    obj.paid = True

                else:

                    obj.paid = False 

                obj.save() 

                messages.success(request,  _("Change made successfully.")) 
            except Exception as e:   
                  messages.error(request, f"Sorry, the following error has occured {e}.")  
         
        
         # deleting an invoice    

         if request.POST.get('id_supprimer'):

            try:

                obj = Facture.objects.get(pk=request.POST.get('id_supprimer'))

                obj.delete()

                messages.success(request, _("The deletion was successful."))   

            except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")   
         items = pagination(request, self.factures)
         self.context['factures'] = items
 
         return render(request,self.templates_name,self.context)

class AddDevisView(View):
    templates_name='html/add-devis.html'
    dataProduct = []
    def get(self, request,*args,**kwargs):
        return render(request ,self.templates_name)
    
    def post(self,request,*args,**kwargs):
        dataProduct = []
        data ={

            'client': request.POST.get('client'),
            'desc': request.POST.get('desc'),
            'produit': request.POST.getlist('produit'),
            'prix': request.POST.getlist('unit'),
            'qantite': request.POST.getlist('qty'),
            'total': request.POST.get('total-a'),
            'all':request.POST.get('all'),
            
        }
        
        try:
          
          if data != '':
             
              messages.success(request,"Devis enregistre avec succes")
             
              print(data)
          else:
              data = {'':''}
              messages.error(request,"sorry, please try again ")
        except Exception as e:
            messages.error(request,f"Sorry our system is {e}")
        # Obj = {'key':'data'}
        
        return render(request,self.templates_name)
    
def get_devis_pdf(request):

    # context={'data':data}
    

    # get html file
    data = request.session.get('data')
   
     # Récupérez l'objet en fonction de son ID
    for produit in data['produit']:  
            pro =  data['produit']
            prix = data['prix']
            qantite = data['qantite']
            total = data['total']
           
    # Faites quelque chose avec les données
    print (data)
    zipped = zip( pro, prix, qantite, total)

    context = {'data': data,'zipped':zipped}
    context['date'] = datetime.datetime.today()
    template = get_template('html/devis-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"
    return response
  

class AddFactureView(View):
    templates_name='html/add-facture.html'
    product = Produit.objects.all()
   
    context ={
        'produits': product
    }
    def get(self,request,*args,**kwags):
        return render( request,self.templates_name, self.context)
    
    @transaction.atomic()
    def post(self,request,*args,**kwags):
       items=[]  
       Qte = Produit.quantity
       

       try:
         client = request.POST.get('client')
         produits = request.POST.getlist('produit')
         qty = request.POST.getlist('qty')
         price = request.POST.getlist('unit')
         total_a = request.POST.getlist('total-a')
         total = request.POST.get('total')
         paid = request.POST.get('paid')
         product = Produit.objects.all()
         print()
         cpt = 0
         for produit_id, qte in zip(produits, qty):
           produit = Produit.objects.get(id=produit_id)
           if int(qte) <= produit.quantity:
               if not paid:
                   paid ='False'
               cpt=cpt+1
               facture_object={
                    'client':client,
                    'save_by' :request.user,
                    'total': total,
                    'paid': paid,
                    
                }
               if cpt == len(produits):
                 facture = Facture.objects.create(**facture_object)
                 for produit_id, qte, prix, total in zip(produits, qty , price,total_a):
          
                   produit = Produit.objects.get(id=produit_id)

                   data = FactureProduct(
                      facture_id = facture.id,
                      produit =  produit,
                      quantity_achat = qte,
                      price_finich = prix,
                      total_a = total,
                    )
                   produit.quantity -= int(qte)
                   produit.total -= int(qte)*produit.price
                   produit.save()
       
         
                    
                 items.append(data)
        
         
                 created = FactureProduct.objects.bulk_create(items) 
                 if created:
            #   produit.quantity -= int(qty)
            #   produit.save()
                  messages.success(request,'data saved seccessfully..')
                 
       
           else:
              messages.error(request, f"Insufficient quantity for {produit.name}")
          
       except Exception as e :
            messages.error(request , f"Error ..{e}")
            #code incomplet Qte n9soha mn bd
       return render(request ,self.templates_name,self.context)
       
class InvoiceVisualizationView(View):
    """ This view helps to visualize the invoice """

    template_name = 'html/facture.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        
        context = get_facture(pk)

        return render(request, self.template_name,context)
#  @superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_facture(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('html/facture-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response

class ConsulterStock(View):
    """ consulter le stock """
    template_name = 'html/consulteStock.html'
    product = Produit.objects.all()
    context={
        'product':product
    }
    def get(self, request, *args, **kwargs):
        product = Produit.objects.all() 
        # obj = Produit.objects.get(nam)
        for produit in product:
            if produit.name.lower() == "regelateur" and produit.quantity < 2 and produit.quantity > 0:
                messages.warning(request,f"la qauntite de {produit.name} presque finie")
            if produit.name.lower() == "lamp 7w" and produit.quantity < 10 and produit.quantity > 0:
                messages.warning(request,f"la qauntite de {produit.name} presque finie")
            if produit.category.lower() == "battrie" and produit.quantity < 2  and produit.quantity > 0:
                messages.warning(request,f"la qauntite de {produit.name} presque finie")
            
        self.context['product'] = product
        return render(request, self.template_name,self.context)
    
    def post(self, request, *args, **kwargs):
      product = Produit.objects.all() 
       
      if request.POST.get('id_sup'):
        try:
          
           obj = Produit.objects.get(pk= request.POST.get('id_sup'))
           print(obj)
           obj.delete()
           messages.success(request, _("The deletion was successful."))   
           product = Produit.objects.all()
           self.context['product'] = product
     
        except Exception as e:
          messages.error(request, f"Sorry, error is : {e}.")  
        
      return render(request, self.template_name,self.context)
class addProduit(View):
    """ add un produit tout sumplement dans un navigateur """

    template_name = 'html/add-produit.html'
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name)
    def post(self,request,*args,**kwargs):
        # if request.POST.get('update'):

        try: 
            name = request.POST.get('title')
            price = request.POST.get('price')
            quantity = request.POST.get('qantite')
            category = request.POST.get('category')
            total = request.POST.get('total')
            print(name,price)
            add_produit={
                'category':category,
                'name':name,
                'quantity':quantity,
                'price': price,
                'total':total,
            }
            created = Produit.objects.create(**add_produit)
            if created:
                  messages.success(request,'data saved seccessfully..')
            else:
                  messages.error(request , 'Sorry Quantite insufisont ..')
           
        except Exception as e:
               messages.error(request,f"Error ....{e}")
        
        return render(request, self.template_name)
        
class vesualiserDevis(View):
    template_name='html/devis.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    def post(self,request,*args,**kwargs):
        data ={

            'client': request.POST.get('client'),
            'desc': request.POST.get('desc'),
            'produit': request.POST.getlist('produit'),
            'prix': request.POST.getlist('unit'),
            'qantite': request.POST.getlist('qty'),
            'total': request.POST.getlist('total-a'),
            'all':request.POST.get('all'),
            
        }
        
        try:
          
          if data != '':
              print(data)
          else:
              data = {'':''}
             
        except Exception as e:
            messages.error(request,f"Sorry our system is {e}")
        # Obj = {'key':'data'}
       
       
        for produit in data['produit']:
          
            pro =  data['produit']
            prix = data['prix']
            qantite = data['qantite']
            total = data['total']
           
    # Faites quelque chose avec les données
        print (data)
        zipped = zip( pro, prix, qantite, total)
        context={'data':data,
                'zipped' : zipped,}
        request.session['data'] = data
        return render(request,self.template_name,context)
    
class misAjour(View):

    templates_name='html/consulteStock.html'
    product = Produit.objects.all()
    context={
        'product':product
    }
    def post(self,request,*args,**kwargs):

        if request.POST.get('delete'):
            try:

                print(request.POST.get('delete'))
                obj = Produit.objects.get(pk= request.POST.get('delete'))
                obj.delete()
                messages.success(request, _("The deletion was successful."))   

            except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")   
        return render(request,self.templates_name,self.context)
    
class upProduit(View):
    product = Produit.objects.all()
    template_name='html/update_product.html'
    context ={
        'product':product
    }
    def get(self,request,*args,**kwargs):
        
         return render(request,self.template_name,self.context)  
      
    def post(self,request,*args,**kwargs):
        print(request.POST.get('update'))
        id = request.POST.get('update')
        if request.POST.get('update'):
            obj = Produit.objects.get(pk= request.POST.get('update'))
            self.context['product'] = obj
        else:
         try:
            title = request.POST.get('title')
            price = request.POST.get('price')
            qantite = request.POST.get('qantite')
            total = request.POST.get('total')
            category = request.POST.get('category')
            obj_secondaire =self.context['product']
            print(obj_secondaire.id)
            obj = Produit.objects.get(pk=obj_secondaire.id)

            obj.category = category
            obj.name = title
            obj.quantity = qantite
            obj.price = price
            obj.total = total
    
            # Sauvegarder les modifications
            obj.save()
            self.context['product'] = obj
            messages.success(request, 'Produit mis à jour avec succès.')
            return redirect('consulte-Stock')
           
         except Exception as e :
             messages.error(request, 'Une erreur s\'est produite lors de la mise à jour du produit : {}'.format(str(e)))
         
        return render(request,self.template_name,self.context)
