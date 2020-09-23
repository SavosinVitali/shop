from django.urls import path, re_path
import mptt_urls
from . import views


app_name = 'category'

urlpatterns = [
# re_path('(?P<product_home_slug>.*)/(?P<product_id>\d{1,})', views.product_detail, name='product_detail'),
re_path('(?P<path>.*)', mptt_urls.view(model='category.models.Category', view='category.views.product_list', slug_field='slug', trailing_slash=True ), name='product_list'),
]
