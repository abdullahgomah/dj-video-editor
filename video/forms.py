from django import forms

class UploadImageForm(forms.Form):
    files = forms.FileField(label='الصور', widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control', 'accept': ".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|image/*"}))



RES_CHOICES= [
    ('facebook', 'إعلان فيسبوك'),
    ('instagram', 'إعلان انستجرام'),
    ('snapchat', 'إعلان سناب شات'),
    ]

class VideoTextForm(forms.Form):
    top_text = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'النص العلوي'}))
    bottom_text = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "النص السفلي"})) 
    time_per_img = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "عدد الثواني لكل صورة"}))
    res = forms.CharField(label='مقاس الفيديو', widget=forms.Select(choices=RES_CHOICES, attrs={"class": 'dropdown show form-control'}))