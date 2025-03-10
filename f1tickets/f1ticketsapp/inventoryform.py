from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'product_id': 'Product_ID',
            'name': 'Name',
            'sku': 'SKU',
            'price': 'Price',
            'quantity': 'Quantity',
            'supplier': 'Supplier',
        }
        widgets = {
            'product_id':forms.NumberInput(
                attrs={'placeholder':'e.g 1', 'class':'form-control'}),
            'name':forms.TextInput(
                attrs={'placeholder':'e.g Australian Grand Prix (General Admission)', 'class':'form-control'}),
            'sku':forms.TextInput(
                attrs={'placeholder':'e.g S00001', 'class':'form-control'}),
            'price':forms.NumberInput(
                attrs={'placeholder':'e.g 200.00', 'class':'form-control'}),
            'quantity':forms.NumberInput(
                attrs={'placeholder':'e.g 110,000', 'class':'form-control'}),
            'supplier':forms.TextInput(
                attrs={'placeholder':'e.g Albert Park Circuit Ticket Office', 'class':'form-control'}),    
        }   