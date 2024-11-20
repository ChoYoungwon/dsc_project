from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Priority

class InfoView(ListView):
    template_name = 'info/info.html'
    model = Priority
    context_object_name = 'object_list'
    paginate_by = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 교통량 구분 필터
        traffic_present = Priority.objects.filter(traffic__isnull=False)
        traffic_absent = Priority.objects.filter(traffic__isnull=True)

        # 페이지 번호 가져오기
        page_present = self.request.GET.get('page_present', 1)
        page_absent = self.request.GET.get('page_absent', 1)

        # 페이지네이션 적용
        paginator_present = Paginator(traffic_present, 10)
        paginator_absent = Paginator(traffic_absent, 10)

        # 각 페이지에 해당하는 객체 가져오기
        traffic_present_page = paginator_present.get_page(page_present)
        traffic_absent_page = paginator_absent.get_page(page_absent)

        # 컨텍스트에 추가
        context['traffic_present'] = traffic_present_page
        context['traffic_absent'] = traffic_absent_page
        return context


class InfoDetailView(DetailView):
    template_name = 'info/info_detail.html'
    model = Priority