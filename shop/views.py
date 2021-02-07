from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})
