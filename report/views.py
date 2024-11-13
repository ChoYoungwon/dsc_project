from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView
from .models import Report
from django.urls import reverse_lazy
from info.tasks import make_priority_table

class ReportCreateView(CreateView):
    template_name = 'report/main.html'
    model = Report
    fields = ['image', 'latitude', 'longitude']
    success_url = reverse_lazy('report:report_success')

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        make_priority_table.delay(form.instance.id)
        return response

class ReportSuccessView(ListView):
    template_name = 'report/report_success.html'
    model = Report
    context_object_name = 'reports'

class MapTestView(TemplateView):
    template_name = 'report/map.html'