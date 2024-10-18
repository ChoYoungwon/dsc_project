from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Report
from django.urls import reverse_lazy

class ReportCreateView(CreateView):
    model = Report
    fields = ['name', 'phone', 'email', 'image', 'latitude', 'longitude']
    success_url = reverse_lazy('report:report_success')

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)

class ReportSuccessView(ListView):
    template_name = 'report/report_success.html'
    model = Report
    context_object_name = 'reports'