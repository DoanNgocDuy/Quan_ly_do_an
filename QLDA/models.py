from django.db import models

# Create your models here.
class Khoa(models.Model):
    Makhoa=models.IntegerField()
    Tenkhoa=models.CharField(max_length=50)
    def __str__(self):
        return self.Tenkhoa
class ChuyenNganh(models.Model):    
    Machuyennganh=models.IntegerField()
    Tenchuyennganh=models.CharField(max_length=50)
    Khoa=models.ForeignKey('Khoa', on_delete=models.RESTRICT, null=True, blank=True)
    def __str__(self):
        return self.Tenchuyennganh
class SinhVien(models.Model):
    Msv=models.CharField(max_length=50)
    Tensv=models.CharField(max_length=50)
    Lop=models.CharField(max_length=50)
    Khoa=models.ForeignKey('Khoa', on_delete=models.RESTRICT, null=True, blank=True)
    ChuyenNganh=models.ForeignKey('ChuyenNganh', on_delete=models.RESTRICT, null=True, blank=True)
    Email=models.CharField(max_length=50)
    So_dien_thoai=models.CharField(max_length=50)
    def __str__(self):
        return self.Tensv
class GiangVien(models.Model):
    Mgv=models.CharField(max_length=50)
    Tengv=models.CharField(max_length=50)
    Khoa=models.ForeignKey('Khoa', on_delete=models.RESTRICT, null=True, blank=True)
    ChuyenNganh=models.ForeignKey('ChuyenNganh', on_delete=models.RESTRICT, null=True, blank=True)
    Email=models.CharField(max_length=50)
    So_dien_thoai=models.CharField(max_length=50)
    def __str__(self):
        return self.Tengv
class DoAn(models.Model):
    Ma_do_an=models.IntegerField()
    Ten_do_an=models.CharField(max_length=255)
    Mo_ta=models.TextField()
    Khoa=models.ForeignKey('Khoa', on_delete=models.RESTRICT, null=True, blank=True)
    ChuyenNganh = models.ForeignKey('ChuyenNganh', on_delete=models.RESTRICT, null=True, blank=True) 
    GiangVien=models.ForeignKey('GiangVien', on_delete=models.RESTRICT, null=True, blank=True)
    So_luong_sv_dk=models.IntegerField(null=True,blank=True,default=None)
    def __str__(self):
        return self.Ten_do_an
class DangKyDoAn(models.Model):
    DoAn=models.ForeignKey('DoAn', on_delete=models.RESTRICT, null=True, blank=True)
    SinhVien=models.ForeignKey('SinhVien', on_delete=models.RESTRICT,null=True, blank=True)
    ThoiGianDangKy=models.DateTimeField(null=True, blank=True,auto_now_add=True)
    nhan_xet_gv = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.DoAn.Ten_do_an +"-"+self.SinhVien.Tensv
class FileDoAn(models.Model):
    dang_ky = models.ForeignKey('DangKyDoAn', on_delete=models.CASCADE, related_name='files_nop' ) 

    file = models.FileField(
        upload_to='bai_nop_do_an/' 
    )
    
    mo_ta_file = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text='Tài liệu'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.dang_ky.SinhVien.Msv}] - {self.file.name.split('/')[-1]}"
