import datetime

from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from administrator.forms import AddressForm, StaffForm
from administrator.models import Assign, Staff, Student
from administrator.views import get_assign
from base.forms import PasswordChangeForm, UserUpdateForm
from staff.decorators import staff_message, staff_required
from staff.forms import AttendenceForm
from staff.models import Attendence

weekday = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


@staff_message
@staff_required
def home_view(request, *args, **kwargs):
    context = {}

    user = request.user
    staff = Staff.objects.filter(user=user).first()

    day_number = datetime.datetime.today().weekday()
    assigns = Assign.objects.filter(teacher=staff, day=weekday[day_number])

    context["assigns"] = assigns
    return render(request, "staff/home.html", context)


@staff_message
@staff_required
def take_attendence_view(request, uuid, *args, **kwargs):
    context = {}

    assign = get_assign(uuid=uuid)
    date = datetime.datetime.today()
    attendence_class = assign.assign_class
    students = Student.objects.filter(current_class=attendence_class)

    attendence_query_list = Attendence.objects.filter(date=date, assign=assign)
    AttendenceFormSet = modelformset_factory(Attendence, AttendenceForm, extra=0)

    if request.method == "GET":
        if attendence_query_list:
            form = AttendenceFormSet(queryset=attendence_query_list)
        else:
            for student in students:
                Attendence.objects.create(assign=assign, student=student, date=date, is_present=False)
            attendence_query_list = Attendence.objects.filter(date=date, assign=assign)
            form = AttendenceFormSet(queryset=attendence_query_list)

    if request.method == "POST":
        form = AttendenceFormSet(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff:home")
        else:
            form = form
            messages.warning(request, "Error...")

    context["form"] = form
    return render(request, "staff/take_attendence.html", context)


@staff_message
@staff_required
def profile_view(request, *args, **kwargs):
    return render(request, "staff/profile.html")


@staff_message
@staff_required
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
            return redirect("staff:profile")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "staff/profile_update.html", context)


@staff_message
@staff_required
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
    return render(request, "staff/password_change.html", context)
