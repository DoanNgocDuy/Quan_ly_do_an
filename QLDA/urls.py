from django.urls import path
from . import views

urlpatterns = [
    path('them_khoa',views.them_khoa,name='them_khoa'),
    path('them_chuyen_nganh',views.them_chuyen_nganh,name='them_chuyen_nganh'),
    path('them_do_an',views.them_do_an,name='them_do_an'),
    path('sua_do_an/<int:pk>',views.sua_do_an,name='sua_do_an'),
    path('xoa_do_an/<int:ma_do_an_id>',views.xoa_do_an,name='xoa_do_an'),
    path('danh_sach_do_an',views.danh_sach_do_an,name='danh_sach_do_an'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('cap_nhat_thong_tin/', views.cap_nhat_thong_tin, name='cap_nhat_thong_tin'),
    path('cap_nhat_thong_tin_sv/', views.cap_nhat_thong_tin_sv, name='cap_nhat_thong_tin_sv'),
    path('cap_nhat_thong_tin_gv/', views.cap_nhat_thong_tin_gv, name='cap_nhat_thong_tin_gv'),
    path('chi-tiet-do-an/<int:pk>/', views.xem_va_dang_ky_do_an, name='chi_tiet_do_an'),
    path('do-an-da-dang-ky/', views.hien_thi_do_an_da_dang_ky, name='do_an_da_dang_ky'),
    path('khoa/', views.danh_sach_khoa, name='danh_sach_khoa'),
    path('chuyen_nganh/', views.danh_sach_chuyen_nganh, name='danh_sach_chuyen_nganh'),
    path('ds_do_an_da_dang_ky/', views.ds_do_an_da_dang_ky_theo_gv, name='ds_do_an_da_dang_ky_gv'),
    path('file/delete/<int:file_id>/', views.delete_submitted_file, name='file_delete'),
    
]
