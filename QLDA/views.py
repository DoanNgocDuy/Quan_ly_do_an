from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.http import require_POST
from .models import SinhVien, GiangVien, DoAn, DangKyDoAn, FileDoAn 
from .forms import FileDoAnForm, TimkiemdoanForm

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def them_khoa(request):
    if request.method == 'POST':
        form = KhoaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm mới khoa thành công")
            return redirect('danh_sach_do_an')
    else:
        form = KhoaForm()
    return render(request, 'them_khoa.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def them_chuyen_nganh(request):
    if request.method == 'POST':
        form = ChuyenNganhForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm mới chuyên ngành thành công")
            return redirect('danh_sach_do_an')
    else:
        form = ChuyenNganhForm()
    return render(request, 'them_chuyen_nganh.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def them_do_an(request):
    if request.method == 'POST':
        form = DoAnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm mới đồ án thành công")
            return redirect('danh_sach_do_an')
    form = DoAnForm()  
    return render(request, 'them_do_an.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def sua_do_an(request, pk):
    do_an = get_object_or_404(DoAn, pk=pk)
    if request.method == 'POST':
        form = DoAnForm(request.POST, instance=do_an)
        if form.is_valid():
            form.save()
            messages.success(request, "Sửa đồ án thành công")
            return redirect('danh_sach_do_an')
    else:
        form = DoAnForm(instance=do_an)
    return render(request, 'sua_do_an.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def xoa_do_an(request,ma_do_an_id):  
    do_an = get_object_or_404(DoAn, id=ma_do_an_id)
    DangKyDoAn.objects.filter(DoAn=do_an).delete()
    do_an.delete()
    messages.success(request, "Xóa đồ án thành công.")
    return redirect("danh_sach_do_an")  

@login_required
def danh_sach_do_an(request):
    form = TimkiemdoanForm(request.GET or None)
    danh_sach_do_an = DoAn.objects.all()  
    if form.is_valid():
        khoa = form.cleaned_data.get('Khoa')
        danh_sach_do_an = danh_sach_do_an.filter(Khoa=khoa)

    return render(request, 'danh_sach_do_an.html', {'form': form, 'danh_sach_do_an': danh_sach_do_an})

    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')      
        password = request.POST.get('password') 

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Sai tên người dùng')
            return redirect('login')  

        user = authenticate(request,username=username, password=password)
        if user is None:
            messages.error(request,'Sai mật khẩu')
            return redirect('login')  
        else:
            login(request, user)
            return redirect('danh_sach_do_an')  
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)  
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
            return redirect('register')  
        else:
            messages.error(request, "❌ Thông tin đăng ký không hợp lệ. Vui lòng kiểm tra lại.")
    else:
        form = UserForm()
 
    return render(request, 'accounts/register.html', {'form': form})

def cap_nhat_thong_tin_sv(request):
 
    if request.method == 'POST':
        form = SinhVienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_do_an')
    else:
        form = SinhVienForm() 

    return render(request, 'cap_nhat_thong_tin_sv.html', {'form': form})

def cap_nhat_thong_tin_gv(request):
   
    if request.method == 'POST':
        form = GiangVienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_do_an')
    else:
        form = GiangVienForm() 

    return render(request, 'cap_nhat_thong_tin_gv.html', {'form': form})

@login_required
def cap_nhat_thong_tin(request):
    try:
        sinh_vien = SinhVien.objects.get(Msv=request.user.username)
        if sinh_vien.Tensv and sinh_vien.So_dien_thoai:
            messages.error(request, "Thông tin sinh viên đã được cập nhật, không thể thay đổi nữa.")
            return redirect('danh_sach_do_an')
    except SinhVien.DoesNotExist:
        sinh_vien = None

    try:
        giang_vien = GiangVien.objects.get(Mgv=request.user.username)
        if giang_vien.Tengv and giang_vien.So_dien_thoai:
            messages.error(request, "Thông tin giảng viên đã được cập nhật, không thể thay đổi nữa.")
            return redirect('danh_sach_do_an')
    except GiangVien.DoesNotExist:
        giang_vien = None
    if request.method == 'POST':
        if 'sinh_vien' in request.POST:
            return redirect('cap_nhat_thong_tin_sv') 
        elif 'giang_vien' in request.POST:
            return redirect('cap_nhat_thong_tin_gv')
    
    return render(request, 'cap_nhat_thong_tin.html')

@login_required
def xem_va_dang_ky_do_an(request, pk):
    do_an = get_object_or_404(DoAn, pk=pk)

    try:
        sinh_vien = SinhVien.objects.get(Msv=request.user.username)
        is_sinh_vien = True
    except SinhVien.DoesNotExist:
        sinh_vien = None
        is_sinh_vien = False

    try:
        giang_vien = GiangVien.objects.get(Mgv=request.user.username)
        is_giang_vien = True
    except GiangVien.DoesNotExist:
        giang_vien = None
        is_giang_vien = False

    if is_giang_vien:
        return render(request, 'chi_tiet_do_an.html', {
            'do_an': do_an,
            'giang_vien_xem': True
        })

    if is_sinh_vien:
        da_dang_ky = DangKyDoAn.objects.filter(SinhVien=sinh_vien).exists()

        if request.method == 'POST':
            if da_dang_ky:
                return render(request, 'chi_tiet_do_an.html', {
                    'do_an': do_an,
                    'error_message': "Bạn chỉ được đăng ký một đồ án duy nhất."
                })
            else:
                dang_ky = DangKyDoAn(SinhVien=sinh_vien, DoAn=do_an)
                dang_ky.save()

                if do_an.So_luong_sv_dk is None:
                    do_an.So_luong_sv_dk = 1  
                else:
                    do_an.So_luong_sv_dk += 1  

                do_an.save()  
                return render(request, 'chi_tiet_do_an.html', {
                    'do_an': do_an,
                    'success_message': "Đăng ký đồ án thành công!"
                })

        return render(request, 'chi_tiet_do_an.html', {
            'do_an': do_an,
            'da_dang_ky': da_dang_ky
        })

    messages.error(request, "Bạn không có quyền truy cập.")
    return redirect('danh_sach_do_an')

@login_required
def hien_thi_do_an_da_dang_ky(request):
    try:
        sinh_vien = SinhVien.objects.get(Msv=request.user.username)
    except SinhVien.DoesNotExist:
        messages.error(request, "Sinh viên không tồn tại.")
        return redirect('danh_sach_do_an')

    do_an_da_dang_ky = DangKyDoAn.objects.filter(SinhVien=sinh_vien).select_related('DoAn').prefetch_related('files_nop') 
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'huy':
            do_an_id = request.POST.get('do_an_id')
            
            dang_ky_can_huy = DangKyDoAn.objects.filter(SinhVien=sinh_vien, DoAn__id=do_an_id).first()

            if dang_ky_can_huy:
                do_an = dang_ky_can_huy.DoAn
                
                dang_ky_can_huy.delete()
                
                do_an.So_luong_sv_dk = (do_an.So_luong_sv_dk or 0) - 1
                if do_an.So_luong_sv_dk <= 0:
                    do_an.So_luong_sv_dk = None 
                do_an.save()
                
                messages.success(request, "Hủy đăng ký đồ án thành công!")
            else:
                messages.error(request, "Không tìm thấy đồ án này trong danh sách đăng ký của bạn.")
            
            return redirect('do_an_da_dang_ky')
        
        elif action == 'nop_file':
            dang_ky_id = request.POST.get('dang_ky_id')
            
            try:
                dang_ky_hien_tai = DangKyDoAn.objects.get(id=dang_ky_id, SinhVien=sinh_vien)
            except DangKyDoAn.DoesNotExist:
                messages.error(request, "Đăng ký không hợp lệ hoặc không thuộc về bạn.")
                return redirect('do_an_da_dang_ky') 

            file_form = FileDoAnForm(request.POST, request.FILES)
            
            if file_form.is_valid():
                new_file = file_form.save(commit=False)
                new_file.dang_ky = dang_ky_hien_tai
                new_file.save()
                messages.success(request, f"Đã nộp file '{new_file.file.name.split('/')[-1]}' thành công.")
            else:
                messages.error(request, "Lỗi nộp file: " + file_form.errors.as_text())
                
            return redirect('do_an_da_dang_ky')
        
        else:
            messages.error(request, "Hành động không hợp lệ.")
            return redirect('do_an_da_dang_ky')


    file_form = FileDoAnForm() 
    
    context = {
        'do_an_da_dang_ky': do_an_da_dang_ky,
        'file_form': file_form,
    }
    return render(request, 'do_an_da_dang_ky.html', context)

def danh_sach_khoa(request):
    ds_khoa = Khoa.objects.all()  
    return render(request, 'danh_sach_khoa.html', {'ds_khoa': ds_khoa})

def danh_sach_chuyen_nganh(request):
    ds_chuyen_nganh = ChuyenNganh.objects.all()
    return render(request, 'danh_sach_chuyen_nganh.html', {'ds_chuyen_nganh': ds_chuyen_nganh})

@login_required
def ds_do_an_da_dang_ky_theo_gv(request):
    try:
        giang_vien = GiangVien.objects.get(Mgv=request.user.username)
    except GiangVien.DoesNotExist:
        messages.error(request, "Lỗi xác thực Giảng viên.")
        return redirect('danh_sach_do_an') 


    if request.method == 'POST':
        action = request.POST.get('action')
        dang_ky_id = request.POST.get('dang_ky_id')
        nhan_xet = request.POST.get('nhan_xet') 
        
        if action == 'luu_nhan_xet_nhanh' and dang_ky_id and nhan_xet is not None:
            try:
                # Lấy đối tượng DangKyDoAn cần cập nhật
                dang_ky_can_cap_nhat = DangKyDoAn.objects.get(
                    id=dang_ky_id,
                    # ... có thể có thêm điều kiện kiểm tra GiangVien ...
                )
                
                # 🔑 Dòng này PHẢI LƯU vào nhan_xet_gv và GỌI .save()
                dang_ky_can_cap_nhat.nhan_xet_gv = nhan_xet.strip() # Dùng nhan_xet_gv
                dang_ky_can_cap_nhat.save() 
                
                # Thêm thông báo thành công nếu cần
                # messages.success(request, "Đã lưu nhận xét thành công.")

            except DangKyDoAn.DoesNotExist:
                # Xử lý lỗi nếu không tìm thấy ID
                pass
                
            # Đảm bảo bạn luôn redirect để tải lại trang

 
            return redirect('ds_do_an_da_dang_ky_gv')
    ds_do_an = DoAn.objects.filter(GiangVien=giang_vien)
    ds_dang_ky = DangKyDoAn.objects.filter(DoAn__in=ds_do_an) \
        .select_related('SinhVien', 'DoAn') \
        .prefetch_related('files_nop') 

    return render(request, 'ds_do_an_da_dang_ky_gv.html', {
        'giang_vien': giang_vien,
        'ds_dang_ky': ds_dang_ky,
    })
@login_required
def upload_file_do_an(request, dang_ky_id):
    dang_ky = get_object_or_404(DangKyDoAn, pk=dang_ky_id)
    if request.method == 'POST':  
        form = FileDoAnForm(request.POST, request.FILES)
        if form.is_valid():
            file_do_an = form.save(commit=False)
            file_do_an.dang_ky = dang_ky 
            file_do_an.save()
            return redirect('trang_chi_tiet_dang_ky', pk=dang_ky_id)
    else:
        form = FileDoAnForm()
    
    return render(request, 'upload_file.html', {'form': form, 'dang_ky': dang_ky})

@login_required
@require_POST
def delete_submitted_file(request, file_id):
    """Xử lý việc xóa file đã nộp."""
    
    file_to_delete = get_object_or_404(FileDoAn, id=file_id)
    

    try:
        sinh_vien = SinhVien.objects.get(Msv=request.user.username)
        if file_to_delete.dang_ky.SinhVien != sinh_vien:
            messages.error(request, "Bạn không có quyền xóa file này.")
            return redirect('do_an_da_dang_ky')
    except SinhVien.DoesNotExist:
        messages.error(request, "Bạn không phải sinh viên có thể xóa file.")
        return redirect('do_an_da_dang_ky')


    try:
        if file_to_delete.file:
            file_to_delete.file.delete(save=False) 
        file_to_delete.delete()
        messages.success(request, f"Đã xóa file thành công.")
        
    except Exception as e:
        messages.error(request, f"Lỗi khi xóa file: Không thể xóa file vật lý hoặc bản ghi.")
    
    return redirect('do_an_da_dang_ky')