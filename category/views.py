from django.shortcuts import render, get_object_or_404

from .forms import BrandAdminForm
from .models import Category, Product


def model_form_upload(request):
    if request.method == 'POST':
        form = BrandAdminForm(request.POST, request.FILES)
        print("model form")
        if form.is_valid():
            form.save()




def product_list(request, path=None, instance=None):
    products = []
    category = None
    if path:
        try:
            category = get_object_or_404(Category, name=instance)
            categories = category.get_descendants(include_self=False).filter(available = True)#get_children()
        #products = category.get_descendants(include_self=False)  Payment.objects.filter(terminal_id__in=[term.terminal_id for term in term_list])
            for cat in category.get_descendants(include_self=True):
                products += Product.published.filter(category=cat)
        except:
            return product_detail(request, path)
        #products = Product.objects.all().filter(category_id=category.id) #vitaskivaem vse produkti
    else:
        categories = Category.objects.all().filter(available = True)
    return render(request, 'category/product/list.html', {'categories': categories, 'category':category, 'path':path, 'instance':instance, 'products': products})


def product_detail(request, path ):
    product = get_object_or_404(Product, slug=path.rsplit('/', maxsplit=1)[1])
    return render(request, 'category/product/detail.html', {'product' : product, 'product_home_slug' : product.slug_home, 'product_id' : product.id })
