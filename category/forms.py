from django import forms
from django.contrib.postgres.fields import JSONField
import json
from django.forms import ModelForm
from category.models import Category, Product, Brand




class BrandAdminForm(ModelForm):

    class Meta:
        model = Brand
        fields = '__all__'

    # def clean_iso(self):
    #     yourfile = self.cleaned_data.get('iso', False)
    #     if yourfile is not False:
    #        print(yourfile.size)
    #        filetype = magic.from_buffer(yourfile.read(2048), mime=True)
    #        if not "application/pdf" in filetype:
    #           raise forms.ValidationError(u'Выберете PDF файл вместо  ' + filetype)
    #     return yourfile

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
