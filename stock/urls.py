from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('' ,views.LoginView.as_view() , name='Login'),
    path('Home' ,views.HomeView.as_view() , name='Home'),
    path('add-devis' , views.AddDevisView.as_view(), name='add-devis'),
    path('add-facture' , views.AddFactureView.as_view(), name='add-facture'),
    path('facture/<int:pk>', views.InvoiceVisualizationView.as_view(), name="facture"),
    path('facture-pdf/<int:pk>', views.get_invoice_pdf, name="facture-pdf"),
    path('consulte-Stock', views.ConsulterStock.as_view(), name="consulte-Stock"),
    path('devis_pdf', views.get_devis_pdf, name="devis_pdf"),
    path('devis', views.vesualiserDevis.as_view(), name="devis"),
    path('add-produit',views.addProduit.as_view(),name='add-produit'),
    path('up-produit',views.upProduit.as_view(),name='up-produit'),

    # path('misAjour', views.misAjour.as_view(), name="misAjour"),

]
urlpatterns+= static(settings.MEDIA_URL,documen_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()