import uuid

import requests
from django.contrib import messages
from django.shortcuts import redirect, render

from accountant.models import Fee, PaymentRecord, StudentFee
from administrator.forms import AddressForm, StudentForm
from administrator.models import Student
from base.forms import PasswordChangeForm, UserUpdateForm
from school.config import KHALTI_TEST_PUBLIC_KEY, KHALTI_TEST_SECRET_KEY
from student.decorators import student_message, student_required
from student.forms import AmountForm


def pay_fee_esewa(student, amount):
    PaymentRecord.objects.create(
        student=student,
        amount=amount,
        method="Esewa",
    )
    student_fee = StudentFee.objects.filter(student=student)[0]
    student_fee.pay_fee(amount=amount)


def pay_fee_khalti(student, paid_amount):
    amount = float(paid_amount) / 100
    PaymentRecord.objects.create(
        student=student,
        amount=amount,
        method="Khalti",
    )
    student_fee = StudentFee.objects.filter(student=student)[0]
    student_fee.pay_fee(amount=amount)


@student_message
@student_required
def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "student/home.html", context)


@student_message
@student_required
def pay_fee_view(request, *args, **kwargs):
    context = {}

    user = request.user
    student = Student.objects.filter(user=user).first()
    payable_fee = Fee.objects.filter(course=student.current_class.course).first()
    paid_fee = StudentFee.objects.get_or_create(student=student)[0]

    total_amount = payable_fee.get_payable_fee()
    payable_amount = total_amount - paid_fee.paid_amount + paid_fee.previous_dues

    amount_form = AmountForm(request.POST or None)
    if request.method == "POST":
        pay_amount = float(request.POST["pay_amount"])
        if pay_amount <= payable_amount:
            pid = uuid.uuid4()
            khalti_public_key = KHALTI_TEST_PUBLIC_KEY
            return render(
                request,
                "student/payment_page.html",
                {
                    "amount": pay_amount,
                    "pid": pid,
                    "test_public_key": khalti_public_key,
                },
            )
        else:
            messages.error(request, "Pay amount must be less than or equal to Payable Amount.")

    context["form"] = amount_form
    context["payable_amount"] = payable_amount
    return render(request, "student/pay_fee.html", context)


@student_message
@student_required
def post_esewa_success_view(request, pid, *args, **kwargs):
    oid = request.GET.get("oid", None)
    amount = request.GET.get("amt", None)
    refId = request.GET.get("refId", None)

    if oid and refId and amount:
        url = "https://uat.esewa.com.np/epay/transrec"
        data = {
            "amt": amount,
            "scd": "EPAYTEST",
            "rid": refId,
            "pid": pid,
        }
        response = requests.post(url, data)
        status_code = str(response.status_code)
        if status_code == "200":
            user = request.user
            student = Student.objects.filter(user=user).first()
            pay_fee_esewa(student=student, amount=amount)
            messages.success(request, "Payment Successfull.")
        else:
            messages.error(request, "Payment Failed.")
    else:
        messages.error(request, "Error in payment...")
    return render(request, "student/payment_result.html")


@student_message
@student_required
def post_esewa_failed_view(request, *args, **kwargs):
    messages.error(request, "Error in initiating payment.")
    return redirect("student:home")


@student_message
@student_required
def post_khalti_success_view(request, *args, **kwargs):
    idx = request.POST.get("idx", None)
    pid = request.POST.get("product_identity", None)
    token = request.POST.get("token", None)
    amount = request.POST.get("amount", None)

    if idx and pid and token and amount:
        key = f"Key {KHALTI_TEST_SECRET_KEY}"
        url = "https://khalti.com/api/v2/payment/verify/"
        headers = {"Authorization": key}
        data = {
            "token": token,
            "amount": amount,
        }
        response = requests.post(url, data=data, headers=headers)
        status_code = str(response.status_code)
        if status_code == "200":
            user = request.user
            student = Student.objects.filter(user=user).first()
            pay_fee_khalti(student=student, paid_amount=amount)
            messages.success(request, "Payment Successfull.")
        else:
            messages.error(request, "Payment Failed.")
    else:
        messages.error(request, "Error in payment...")
    return render(request, "student/payment_result.html")


@student_message
@student_required
def post_khalti_failed_view(request, *args, **kwargs):
    messages.error(request, "Error in initiating payment.")
    return redirect("student:home")


@student_message
@student_required
def profile_view(request, *args, **kwargs):
    return render(request, "student/profile.html")


@student_message
@student_required
def profile_update_view(request, *args, **kwargs):
    context = {}
    user = request.user
    student = Student.objects.get(user=user)

    u_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=student.user)
    s_form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    pa_form = AddressForm(request.POST or None, instance=student.permanent_address)
    ca_form = AddressForm(request.POST or None, instance=student.current_address)

    if request.method == "POST":
        if u_form.is_valid() and s_form.is_valid() and pa_form.is_valid() and ca_form.is_valid():
            user = u_form.save()
            p_address = pa_form.save()
            c_address = ca_form.save()
            student = s_form.save()
            student.user = user
            student.permanent_address = p_address
            student.current_address = c_address
            student.save()
            messages.success(request, f"Profile updated successfully.")
            return redirect("student:profile")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "student/profile_update.html", context)


@student_message
@student_required
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
    return render(request, "student/password_change.html", context)
