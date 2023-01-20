from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import redirect, render

from administrator.decorators import administrator_message, administrator_required
from administrator.forms import AddressForm, StudentForm
from administrator.models import Student
from base.forms import RegistrationForm, UserUpdateForm
from school.tasks import send_user_activation_email


def get_student(uuid):
    try:
        student = Student.objects.get(id=uuid)
        return student
    except Student.DoesNotExist:
        return None


@administrator_message
@administrator_required
def create_student_view(request, *args, **kwargs):
    context = {}

    u_form = RegistrationForm(request.POST or None, request.FILES or None)
    s_form = StudentForm(request.POST or None, request.FILES or None)
    pa_form = AddressForm(request.POST or None)
    ca_form = AddressForm(request.POST or None)

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

            messages.success(request, f"Student created successfully.")
            return redirect("administrator:student-list")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["action"] = "Create"
    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "administrator/student/student_form.html", context)


@administrator_message
@administrator_required
def list_student_view(request, *args, **kwargs):
    context = {}

    if request.method == "GET":
        students = Student.objects.all()

    if request.method == "POST":
        if "search" in request.POST:
            text = request.POST["search"]
            students = Student.objects.filter(Q(user__email__icontains=text) | Q(user__name__icontains=text))

    context["students"] = students
    return render(request, "administrator/student/student_list.html", context)


@administrator_message
@administrator_required
def detail_student_view(request, uuid, *args, **kwargs):
    context = {}
    student = get_student(uuid=uuid)
    context["student"] = student
    return render(request, "administrator/student/student_detail.html", context)


@administrator_message
@administrator_required
def update_student_view(request, uuid, *args, **kwargs):
    context = {}
    student = get_student(uuid=uuid)

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
            messages.success(request, f"Student updated successfully.")
            return redirect("administrator:student-list")

        else:
            u_form, s_form, pa_form, ca_form = u_form, s_form, pa_form, ca_form
            messages.error(request, "Error.")

    context["action"] = "Update"
    context["u_form"] = u_form
    context["s_form"] = s_form
    context["pa_form"] = pa_form
    context["ca_form"] = ca_form
    return render(request, "administrator/student/student_form.html", context)


@administrator_message
@administrator_required
def delete_student_view(request, uuid, *args, **kwargs):
    student = get_student(uuid=uuid)
    name = student.user.name

    if request.method == "POST":
        student.user.delete()
        student.permanent_address.delete()
        student.current_address.delete()
        student.delete()
        messages.success(request, f"Student {name} is deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:student-list")
