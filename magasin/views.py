from django.shortcuts import redirect, render , get_object_or_404
from .models import Produit
from .models import Fournisseur
from .forms import ProduitForm,ProductForm, FournisseurForm,UserRegistrationForm,UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
 
from magasin.models import Categorie    
from magasin.serializers import CategorySerializer
from magasin.models import Produit,Product
from magasin.serializers import ProduitsSerializer
from rest_framework import viewsets


class ProductViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProduitsSerializer

    def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset

def CatalogueProduct(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/catalogue.html', context)




def CreateProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            products = Product.objects.all()
            return render(request, 'store/catalogue.html', {'products': products})
    else:
        form = ProductForm()  # créer formulaire vide
        products = Product.objects.all()
        return render(request, 'store/create_product.html', {'form': form, 'products': products})



class ProduitAPIView(APIView):
 
    def get(self, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitsSerializer(produits, many=True)
        return Response(serializer.data)
class CategoryAPIView(APIView):
 
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

def index(request):
       if request.method == "POST" :
         form = ProduitForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              list=Produit.objects.all()
              return render(request,'Produits/vitrineP.html',{'list':list})
       else : 
            form = ProduitForm() #créer formulaire vide 
            list=Produit.objects.all()
            return render(request,'Produits/create_product.html',{'form':form,'list':list})

def indexA(request):
     return render(request,'magasin/acceuil.html' )


def ListFournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'Fournisseurs/mesFournisseurs.html', context)

def nouveauFournisseur(request):
    if request.method == "POST" :
         form = FournisseurForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              nouvFournisseur=Fournisseur.objects.all()
              return render(request,'Fournisseurs/vitrineF.html',{'nouvFournisseur':nouvFournisseur})
    else : 
            form = FournisseurForm() #créer formulaire vide 
            nouvFournisseur=Fournisseur.objects.all()
            return render(request,'Fournisseurs/create_For.html',{'form':form,'nouvFournisseur':nouvFournisseur})
def Catalogue(request):
        products= Produit.objects.all()
        context={'products':products}
        return render( request,'Produits/mesProduits.html',context )

def register(request):
     if request.method == 'POST' :
          form = UserCreationForm(request.POST)
          if form.is_valid():
               form.save()
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password1')
               user = authenticate(username=username, password=password)
               login(request,user)
               messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
               return redirect('home')
     else :
          form = UserCreationForm()
     return render(request,'registration/register.html',{'form' : form})

class ChangePasswordView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('home')


def edit_product(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            produit = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['img']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                produit.img = nouvelle_image
            # Sauvegarder le produit
            produit.save()
            return redirect('Catalogue')
    else:
        form = ProduitForm(instance=product)
        return render(request, 'Produits/edit_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('Catalogue')
    return render(request, 'Produits/delete_product.html', {'product': product})

def detail_product(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    context = {'produit': produit}
    return render(request, 'Produits/detail_product.html', context)



def edit_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, request.FILES, instance=fournisseur)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo= nouvelle_image
            # Sauvegarder le produit
            frns.save()
            return redirect('fournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)
        return render(request, 'Fournisseurs/edit_For.html', {'form': form})

def delete_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseurs')
    return render(request,'Fournisseurs/delete_For.html', {'fournisseur': fournisseur})

def detail_Fournisseur(request, for_id):
    fournisseur = get_object_or_404(Fournisseur, id=for_id)
    context = {'fournisseur': fournisseur}
    return render(request, 'Fournisseurs/detail_For.html', context)




from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)