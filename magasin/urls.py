from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CategoryAPIView
from .views import ProduitAPIView


urlpatterns = [
    
    path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('products/', views.index, name='index'),
    path('CatalogueProduct/', views.CatalogueProduct, name='CatalogueProduct'),
   path('CreateProduct/', views.CreateProduct, name='CreateProduct'),
   
    path('', views.indexA, name='indexA'),
    path('fournisseurs/', views.ListFournisseur, name='fournisseurs'),
    path('Catalogue/', views.Catalogue, name='Catalogue'),
    path('nouvFournisseur/',views.nouveauFournisseur,name='nouvFournisseur'),
    path('register/',views.register, name = 'register'), 
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),

    path('editFournisseur/<int:fk>/', views.edit_Fournisseur, name='edit_Fournisseur'),
    path('deleteFournisseur/<int:fk>/', views.delete_Fournisseur, name='delete_Fournisseur'),
    path('Fournisseur/<int:for_id>/', views.detail_Fournisseur, name='detail_Fournisseur'),

    path('editProduct/<int:pk>/', views.edit_product, name='edit_product'),
    path('deleteProduct/<int:pk>/', views.delete_product, name='delete_product'),
    path('Product/<int:product_id>/', views.detail_product, name='detail_product'),
    path('api/category/', CategoryAPIView.as_view()),
    path('api/produits/', ProduitAPIView.as_view()),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)