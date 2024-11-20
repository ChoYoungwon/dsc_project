from django import forms
from .models import Report

class GPSInputForm(forms.ModelForm):
    latitude = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': '위도'}))
    longitude = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': '경도'}))
    class Meta:
        model = Report
        fields = ['latitude', 'longitude']
        widgets = {
            'latitude': forms.NumberInput(attrs={'placeholder': '위도'}),
            'longitude': forms.NumberInput(attrs={'placeholder': '경도'}),
        }

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')  # get()을 사용해 KeyError 방지
        print(f"Latitude before cleaning: {latitude}")
        if latitude in (None, ''):  # 값이 없으면 None 반환
            return None
        try:
            return float(latitude)
        except ValueError:
            raise forms.ValidationError("위도가 잘못된 형식입니다. 숫자를 입력해주세요.")

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')  # get()을 사용해 KeyError 방지
        print(f"Longitude before cleaning: {longitude}")
        if longitude in (None, ''):  # 값이 없으면 None 반환
            return None
        try:
            return float(longitude)
        except ValueError:
            raise forms.ValidationError("경도가 잘못된 형식입니다. 숫자를 입력해주세요.")