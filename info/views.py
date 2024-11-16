from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Priority

class InfoView(ListView):
    template_name = 'info/info.html'
    model = Priority
    context_object_name = 'object_list'
    paginate_by = 10

class InfoDetailView(DetailView):
    template_name = 'info/info_detail.html'
    model = Priority