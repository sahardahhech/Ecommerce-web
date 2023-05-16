from rest_framework.serializers import ModelSerializer
 
from magasin.models import Categorie
from magasin.models import Produit
 
class CategorySerializer(ModelSerializer):
 
    class Meta:
        model = Categorie
        fields = ['id', 'name']

class ProduitsSerializer(ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'libellé','description','id.categorie']

 