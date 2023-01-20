from django.contrib import messages
from django.db.models.query import Q
from django.shortcuts import redirect, render

from accountant.decorators import accountant_message, accountant_required
from accountant.models import Fee, PaymentRecord, StudentFee
from administrator.forms import AddressForm, StaffForm
from administrator.models import Staff, Student
from administrator.views_student import get_student
from base.forms import PasswordChangeForm, UserUpdateForm
from student.forms import AmountForm


@accountant_message
@accountant_required
def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "accountant/home.html", context)


@accountant_message
@accountant_required
def list_student_view(request, *args, **kwargs):
    context = {}

    if request.method == "GET":
        students = Student.objects.all()

    if request.method == "POST":
        if "search" in request.POST:
            text = request.POST["search"]
            students = Student.objects.filter(Q(user__email__icontains=text) | Q(user__name__icontains=text))

    context["students"] = students
    return render(request, "accountant/student_list.html", context)


@accountant_message
@accountant_required
def pay_fee_view(request, uuid, *args, **kwargs):
    context = {}
    student = get_student(uuid=uuid)

    payable_fee = Fee.objects.filter(course=student.current_class.course).first()
    paid_fee = StudentFee.objects.get_or_create(student=student)[0]

    total_amount = payable_fee.get_payable_fee()
    payable_amount = total_amount - paid_fee.paid_amount + paid_fee.previous_dues

    amount_form = AmountForm(request.POST or None)
    if request.method == "POST":
        pay_amount = float(request.POST["pay_amount"])
        if pay_amount <= payable_amount:
            PaymentRecord.objects.create(student=student, amount=pay_amount)
            student_fee = StudentFee.objects.filter(student=student)[0]
            student_fee.pay_fee(amount=pay_amount)
            messages.success(request, "Fee payment successfull.")
            return redirect("accountant:list-student")
        else:
            messages.error(request, "Pay amount must be less than or equal to Payable Amount.")

    context["form"] = amount_form
    context["payable_amount"] = payable_amount

    return render(request, "accountant/pay_fee.html", context)


@accountant_message
@accountant_required
def profile_view(request, *args, **kwargs):
    return render(request, "accountant/profile.html")


@accountant_message
@accountant_required
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
            return redirect("accountant:profile")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "accountant/profile_update.html", context)


@accountant_message
@accountant_required
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
    return render(request, "accountant/password_change.html", context)
