from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import redirect, render

from administrator.decorators import administrator_message, administrator_required
from administrator.forms import AddressForm, StaffForm
from administrator.models import Staff
from base.forms import PasswordChangeForm, RegistrationForm, UserUpdateForm
from school.tasks import send_user_activation_email


def get_staff(uuid):
    try:
        staff = Staff.objects.get(id=uuid)
        return staff
    except Staff.DoesNotExist:
        return None


@administrator_message
@administrator_required
def create_staff_view(request, *args, **kwargs):
    context = {}

    u_form = RegistrationForm(request.POST or None, request.FILES or None)
    s_form = StaffForm(request.POST or None, request.FILES or None)
    pa_form = AddressForm(request.POST or None)
    ca_form = AddressForm(request.POST or None)

    if request.method == "POST":
        if u_form.is_valid() and s_form.is_valid() and pa_form.is_valid() and ca_form.is_valid():
            user = u_form.save()
            p_address = pa_form.save()
            c_address = ca_form.save()
            staff = s_form.save()
            staff.user = user
            staff.permanent_address = p_address
            staff.current_address = c_address
            staff.save()

            user.username = user.email.split("@")[0]
            user.save()

            # site = get_current_site(request)
            # domain = site.domain
            # send_user_activation_email(user.id, domain)
            # # send_user_activation_email.delay(user.id, domain)
            # messages.success(
            #     request,
            #     f"An email with verification link is sent to your Email ID. Verify Your account before login.",
            # )

            messages.success(request, f"Staff created successfully.")
            return redirect("administrator:staff-list")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["action"] = "Create"
    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "administrator/staff/staff_form.html", context)


@administrator_message
@administrator_required
def list_staff_view(request, *args, **kwargs):
    context = {}

    if request.method == "GET":
        staffs = Staff.objects.all()

    if request.method == "POST":
        if "search" in request.POST:
            text = request.POST["search"]
            staffs = Staff.objects.filter(Q(user__email__icontains=text) | Q(user__name__icontains=text))

    context["staffs"] = staffs
    return render(request, "administrator/staff/staff_list.html", context)


@administrator_message
@administrator_required
def detail_staff_view(request, uuid, *args, **kwargs):
    context = {}
    staff = get_staff(uuid=uuid)
    context["staff"] = staff
    return render(request, "administrator/staff/staff_detail.html", context)


@administrator_message
@administrator_required
def update_staff_view(request, uuid, *args, **kwargs):
    context = {}
    staff = get_staff(uuid=uuid)

    u_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=staff.user)
    s_form = StaffForm(request.POST or None, request.FILES or None, instance=staff)
    pa_form = AddressForm(request.POST or None, instance=staff.permanent_address)
    ca_form = AddressForm(request.POST or None, instance=staff.current_address)

    if request.method == "POST":
        if u_form.is_valid() and s_form.is_valid() and pa_form.is_valid() and ca_form.is_valid():
            user = u_form.save()
            p_address = pa_form.save()
            c_address = ca_form.save()
            staff = s_form.save()
            staff.user = user
            staff.permanent_address = p_address
            staff.current_address = c_address
            staff.save()
            messages.success(request, f"Staff updated successfully.")
            return redirect("administrator:staff-list")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["action"] = "Update"
    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "administrator/staff/staff_form.html", context)


@administrator_message
@administrator_required
def delete_staff_view(request, uuid, *args, **kwargs):
    staff = get_staff(uuid=uuid)
    name = staff.user.name

    if request.method == "POST":
        staff.user.delete()
        staff.permanent_address.delete()
        staff.current_address.delete()
        staff.delete()
        messages.success(request, f"Staff {name} is deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:staff-list")


@administrator_message
@administrator_required
def profile_view(request, *args, **kwargs):
    return render(request, "administrator/profile.html")


@administrator_message
@administrator_required
def profile_update_view(request, *args, **kwargs):
    context = {}
    user = request.user
    staff = Staff.objects.get(user=user)

    u_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=staff.user)
    s_form = StaffForm(request.POST or None, request.FILES or None, instance=staff)
    pa_form = AddressForm(request.POST or None, instance=staff.permanent_address)
    ca_form = AddressForm(request.POST or None, instance=staff.current_address)

    if request.method == "POST":
        if u_form.is_valid() and s_form.is_valid() and pa_form.is_valid() and ca_form.is_valid():
            user = u_form.save()
            p_address = pa_form.save()
            c_address = ca_form.save()
            staff = s_form.save()
            staff.user = user
            staff.permanent_address = p_address
            staff.current_address = c_address
            staff.save()
            messages.success(request, f"Profile updated successfully.")
            return redirect("administrator:profile")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "administrator/profile_update.html", context)


@administrator_message
@administrator_required
def password_change_view(request, *args, **kwargs):
    context = {}

    user = request.user
    form = PasswordChangeForm(user, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Password changed successfully. Please login with new password to continue.")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    return render(request, "administrator/password_change.html", context)
