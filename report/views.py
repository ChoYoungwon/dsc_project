from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, FormView, DetailView, TemplateView
from .models import Report
from django.urls import reverse_lazy
from info.tasks import make_priority_table
from .utils import extract_gps_info
from django.urls import reverse
from .forms import GPSInputForm

class ReportCreateView(CreateView):
    template_name = 'report/main.html'
    model = Report
    fields = ['image']

    def get_success_url(self):
        return reverse_lazy('report:report_success', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        print("Form is invalid in createView")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        image = form.cleaned_data['image']

        # 메타 데이터 추출, 성공시 위도 경도 반환, 실패시 None 반환
        gps_info = extract_gps_info(image)
        self.object = form.save(commit=False)

        # 위치 데이터가 있는 경우 위도 경도를 저장한다.
        if gps_info:
            self.object.latitude, self.object.longitude = gps_info
        else:
            # 전달된 값이 없으면, 기본 QueryDict에서 값을 가져옵니다.
            latitude = self.request.POST.get('latitude')
            longitude = self.request.POST.get('longitude')

            if latitude and longitude:
                self.object.latitude = latitude
                self.object.longitude = longitude
            else:
                # 이 경우에도 여전히 None이면(위도 경도가 없는 경우) enter_gps로 리디렉션한다.
                self.object.latitude = None
                self.object.longitude = None
                self.object.save()
                self.request.session['alert_message'] = '사진의 메타 데이터에 위치 정보가 없습니다.\n도로 파손 위치를 지정해 주세요'
                # gps를 입력받는 페이지로 리디렉션
                return redirect(reverse('report:enter_gps', kwargs={'pk': self.object.pk}))

        self.object.save()
        make_priority_table.delay(form.instance.id)
        return super().form_valid(form)

class ReportCreateView2(FormView):
    template_name = 'report/enter_gps.html'
    form_class = GPSInputForm

    def get_success_url(self):
        return reverse_lazy('report:report_success', kwargs={'pk': self.kwargs['pk']})

    # Url에서 전달된 pk로 객체를 가져와 초기값을 설정
    def get_form(self, *args, **kwargs):
        self.object = get_object_or_404(Report, pk=self.kwargs['pk'])
        form = self.form_class(instance=self.object, **self.get_form_kwargs())
        print("Initialized form data:", form.initial)  # 폼의 초기값 확인
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_url'] = self.object.image.url if self.object.image else None
        context['pk'] = self.object.pk
        return context

    def form_valid(self, form):
        self.object = form.save()
        print(f"Saved Report: {self.object}")
        print(f"Latitude: {self.object.latitude}, Longitude: {self.object.longitude}")
        make_priority_table.delay(self.object.id)

        success_url = self.get_success_url()
        print(f"Redirecting to {success_url}")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid in ReportCreateView2")
        print("Form errors:", form.errors)  # 폼의 에러 메시지 출력
        print("POST data:", self.request.POST)  # 전달된 데이터를 확인
        return super().form_invalid(form)

class ReportSuccessView(DetailView):
    template_name = 'report/report_success.html'
    model = Report
    context_object_name = 'reports'

class MapTestView(TemplateView):
    template_name = 'report/map.html'