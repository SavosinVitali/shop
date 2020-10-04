from django import forms
from django.contrib.postgres.fields import JSONField
import json
from django.forms import ModelForm
from category.models import Category, Product, Brand

class BrandAdminForm(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def clean_logo(self):
        data = self.cleaned_data['logo']
        print('logo')
        print(self)
        return data

    def clean_name(self):
        data = self.cleaned_data['name']
        print('name')
        print(data)
        return data

class ProductAdminForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class CategoryAdminForm(ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        # widgets = {
        #     'attributes': JSONEditorWidget(dynamic_schema_product, True)
        # }

    # class Media:
    #     css = { "all" : ("css/admin_atributes.css",) }
