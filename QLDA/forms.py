from django import forms
from .models import *
from django.contrib.auth.models import User
class KhoaForm(forms.ModelForm):
    class Meta:
        model = Khoa
        fields = '__all__'
        labels = {
            'Makhoa': 'Mã khoa',
            'Tenkhoa': 'Tên khoa',
        }
class ChuyenNganhForm(forms.ModelForm):
    class Meta:
        model = ChuyenNganh
        fields = '__all__'
        labels = {
            'Machuyennganh': 'Mã chuyên ngành',
            'Tenchuyennganh': 'Tên chuyên ngành',
            'Khoa': 'Khoa',
            
        }
class SinhVienForm(forms.ModelForm):
    class Meta:
        model = SinhVien
        fields = '__all__'
        labels = {
            'Msv': 'Mã sinh viên',
            'Tensv': 'Tên sinh viên',
            'Lop': 'Lớp',
            'Email': 'Email',
            'So_dien_thoai': 'Số điện thoại',
        }
class GiangVienForm(forms.ModelForm):
    class Meta:
        model = GiangVien
        fields = '__all__'
        labels = {
            'Mgv': 'Mã giảng viên',
            'Tengv': 'Tên giảng viên',
            'Email': 'Email',
            'So_dien_thoai': 'Số điện thoại',
        }
class DoAnForm(forms.ModelForm):
    class Meta:
        model = DoAn
        fields = '__all__'
        labels = {
            'Ma_do_an': 'Mã đồ án',
            'Ten_do_an': 'Tên đồ án',
            'Mo_ta': 'Mô tả',
            'Khoa': 'Khoa',
            'ChuyenNganh': 'Chuyên ngành',
            'GiangVien': 'Giảng viên',
        }
        exclude = ['So_luong_sv_dk']
class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={'placeholder': 'Nhập mật khẩu','class': 'input-text'})
    )
    password2 = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={'placeholder': 'Nhập lại mật khẩu','class': 'input-text'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {'username': 'Tên người dùng'}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nhập tên người dùng','class': 'input-text'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = ""

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("⚠️ Tên người dùng đã tồn tại. Vui lòng chọn tên khác.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("⚠️ Hai mật khẩu không khớp nhau.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class TimkiemdoanForm(forms.Form):
    Khoa = forms.ModelChoiceField(
        queryset=Khoa.objects.all(),
        required=False,
        label='Chọn khoa',
    )
class FileDoAnForm(forms.ModelForm):
    class Meta:
        model = FileDoAn
        # Chỉ cần hiển thị trường file và mô tả
        fields = ('file', 'mo_ta_file',)