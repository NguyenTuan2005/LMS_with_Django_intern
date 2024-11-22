from django.shortcuts import render, get_object_or_404, redirect
from role.models import Role
from role.forms import RoleForm, ExcelImportForm
import pandas as pd
from django.contrib import messages
from django.http import HttpResponse
import openpyxl
from module_group.models import ModuleGroup, Module
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import Profile
from .admin import RoleResource
from tablib import Dataset
from django.core.files.uploadedfile import UploadedFile

def role_list(request):
    roles = Role.objects.all()  # Lấy danh sách các role
    module_groups = ModuleGroup.objects.all()  # Thay đổi theo cách bạn lấy dữ liệu
    grouped_modules = {group: group.modules.all() for group in module_groups}

    form = ExcelImportForm()

    return render(request, 'role_list.html', { 'roles': roles, 'form': form,
        'module_groups': module_groups,
        'grouped_modules': grouped_modules
    })

def insert_role(role_id, role_name):
    try:
        Role.objects.create(
            role_id=role_id,
            role_name=role_name
        )
        return True, None
    except Exception as e:
        return False, str(e)


def role_add(request, role_id=None):
    if role_id:  # Nếu role_id được cung cấp, tức là đang chỉnh sửa một role hiện có
        role = get_object_or_404(Role, id=role_id)
        form = RoleForm(request.POST or None, instance=role)
    else:  # Nếu không có role_id, tức là đang thêm một role mới
        role = None
        form = RoleForm(request.POST or None)

    # Lấy danh sách tất cả permissions và modules
    specific_permissions = Role._meta.permissions
    all_permissions = Permission.objects.filter(
        codename__in=[codename for codename, _ in specific_permissions]
    )
    all_modules = Module.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            new_role = form.save()
            selected_permissions = request.POST.getlist('permissions')
            selected_modules_ids = request.POST.getlist('modules')

            # Cập nhật permissions và modules cho role
            new_role.permissions.set(Permission.objects.filter(id__in=selected_permissions))
            new_role.modules.set(Module.objects.filter(id__in=selected_modules_ids))
            new_role.save()

            # Thêm thông báo thành công
            messages.success(request, 'Role and associated permissions/modules added/updated successfully.')
            return redirect('role:role_list')

    # Xác định permissions và modules đã được chọn
    selected_permissions = role.permissions.all() if role else []
    selected_modules = role.modules.all() if role else []

    context = {
        'form': form,
        'all_permissions': all_permissions,
        'selected_permissions': selected_permissions,
        'all_modules': all_modules,
        'selected_modules': selected_modules,
    }
    return render(request, 'role_form.html', context)
def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    
    # Lấy danh sách tất cả permissions và modules
    specific_permissions = Role._meta.permissions
    all_permissions = Permission.objects.filter(
        codename__in=[codename for codename, _ in specific_permissions]
    )
    all_modules = Module.objects.all()

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()  # Lưu role

            # Lấy danh sách permission và module đã chọn
            selected_permissions = request.POST.getlist('permissions')
            selected_modules_ids = request.POST.getlist('modules')

            # Cập nhật permissions và modules cho role
            role.permissions.set(Permission.objects.filter(id__in=selected_permissions))
            role.modules.set(Module.objects.filter(id__in=selected_modules_ids))
            role.save()

            messages.success(request, 'Role, permissions, and modules updated successfully.')
            return redirect('role:role_list')
    else:
        form = RoleForm(instance=role)

    # Xác định permissions và modules đã được chọn
    selected_permissions = role.permissions.all()
    selected_modules = role.modules.all()

    context = {
        'form': form,
        'all_permissions': all_permissions,
        'selected_permissions': selected_permissions,
        'all_modules': all_modules,
        'selected_modules': selected_modules,
    }
    return render(request, 'role_form.html', context)


def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role:role_list')
    return render(request, 'role_confirm_delete.html', {'role': role})



from .admin import RoleResource

def export_roles(request):
    # Tạo resource
    resource = RoleResource()
    queryset = Role.objects.all()

    # Xuất dữ liệu
    dataset = resource.export(queryset)

    # Tạo phản hồi với định dạng Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=lms_roles.xlsx'

    # Ghi dữ liệu vào phản hồi dưới dạng XLSX
    response.write(dataset.xlsx)  # Đảm bảo sử dụng đúng phương thức để xuất ra xlsx

    return response



def import_roles(request):
    resource = RoleResource()

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        # Kiểm tra xem file có được tải lên không
        if not uploaded_file:
            messages.error(request, "Không tìm thấy tệp tin để nhập.")
            return redirect('role:role_list')

        if uploaded_file.size == 0:  # Kiểm tra nếu tệp rỗng
            messages.error(request, "Tệp không được để trống.")
            return redirect('role:role_list')

        file_format = uploaded_file.name.split('.')[-1].lower()
        dataset = Dataset()

        # Xử lý định dạng tệp
        formats = {
            'csv': lambda: dataset.load(uploaded_file.read().decode('utf-8'), format='csv'),
            'json': lambda: dataset.load(uploaded_file.read().decode('utf-8'), format='json'),
            'yaml': lambda: dataset.load(uploaded_file.read().decode('utf-8'), format='yaml'),
            'tsv': lambda: dataset.load(uploaded_file.read().decode('utf-8'), format='tsv'),
            'xlsx': lambda: dataset.load(uploaded_file.read(), format='xlsx'),
        }

        # Kiểm tra và xử lý tệp
        try:
            if file_format in formats:
                formats[file_format]()  # Gọi hàm xử lý định dạng
            else:
                messages.error(request, "Định dạng tệp không hợp lệ. Hỗ trợ các định dạng: csv, json, yaml, tsv, xlsx.")
                return redirect('role:role_list')
        except Exception as e:
            messages.error(request, f"Lỗi khi đọc tệp: {e}")
            return redirect('role:role_list')

        # Kiểm tra và nhập dữ liệu
        result = resource.import_data(dataset, dry_run=True)

        if not result.has_validation_errors():
            resource.import_data(dataset, dry_run=False)
            messages.success(request, "Người dùng đã được nhập thành công!")
        else:
            invalid_rows = result.invalid_rows
            error_messages = [f"Lỗi tại hàng {row['row']}: {row['error']}" for row in invalid_rows]
            messages.error(request, "Có lỗi khi nhập người dùng:\n" + "\n".join(error_messages))

        return redirect('role:role_list')

    messages.error(request, "Không thể nhập người dùng.")
    return redirect('role:role_list')


@login_required
def select_role(request):
    if request.method == 'POST':
        selected_role_name = request.POST.get('role')  # Lấy role_name thay vì id
        if selected_role_name:
            try:
                role = Role.objects.get(role_name=selected_role_name)
                if request.user.is_superuser:
                    request.session['temporary_role'] = role.role_name
                    messages.success(request, "Vai trò tạm thời đã được lưu.")
                else:
                    profile = Profile.objects.get(user=request.user)
                    profile.role = role
                    profile.save()
                    messages.success(request, "Vai trò đã được cập nhật.")
            except Role.DoesNotExist:
                messages.error(request, "Vai trò không tồn tại.")
            except Profile.DoesNotExist:
                messages.error(request, "User này chưa có hồ sơ.")
        else:
            messages.warning(request, "Vui lòng chọn một vai trò.")
    return redirect('main:home')



@login_required
@user_passes_test(lambda u: u.is_superuser)
def reset_role(request):
    if request.method == 'POST':
        # Xóa role tạm thời khỏi session
        if 'temporary_role' in request.session:
            del request.session['temporary_role']
            messages.success(request, "Vai trò tạm thời đã được đặt lại. Bạn đã khôi phục quyền superuser.")
        else:
            messages.info(request, "Không có vai trò tạm thời nào để đặt lại.")

    return redirect('main:home')


def role_permissions(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    specific_permissions = Role._meta.permissions
    all_permissions = Permission.objects.filter(
        codename__in=[codename for codename, _ in specific_permissions]
    )
    
    all_modules = Module.objects.all()
    selected_modules = role.modules.all()
    
    if request.method == "POST":
        selected_permissions = request.POST.getlist('permissions')
        selected_modules_ids = request.POST.getlist('modules')
        
        # Update permissions and modules for the role
        role.permissions.set(Permission.objects.filter(id__in=selected_permissions))
        role.modules.set(Module.objects.filter(id__in=selected_modules_ids))
        role.save()

        # Add a success message
        messages.success(request, 'Permissions and modules updated successfully.')

        # Redirect to role list after saving
        return redirect('role:role_list')

    context = {
        'role': role,
        'all_permissions': all_permissions,
        'selected_permissions': role.permissions.all(),
        'all_modules': all_modules,
        'selected_modules': selected_modules,
    }
    return render(request, 'role_permission.html', context)
