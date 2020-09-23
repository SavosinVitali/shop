from django import template
from ..models import Category, Product

register = template.Library()

@register.inclusion_tag('admin/category_product.html')
def display_category_product(document_id):
    products = Product.objects.filter(category_id=document_id)
    return { 'products': products }
