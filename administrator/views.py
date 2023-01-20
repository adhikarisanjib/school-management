from django.contrib import messages
from django.shortcuts import redirect, render

from accountant.forms import FeeForm
from accountant.models import Fee
from administrator.decorators import administrator_message, administrator_required
from administrator.forms import (
    AcademicSessionForm,
    AssignForm,
    ClassForm,
    CourseForm,
    DepartmentForm,
    SubjectForm,
    TimeSlotForm,
)
from administrator.models import (
    AcademicSession,
    Assign,
    Class,
    Course,
    Department,
    Subject,
    TimeSlot,
)


def get_adademic_session(uuid):
    try:
        academic_session = AcademicSession.objects.get(id=uuid)
        return academic_session
    except AcademicSession.DoesNotExist:
        return None


def get_department(uuid):
    try:
        department = Department.objects.get(id=uuid)
        return department
    except Department.DoesNotExist:
        return None


def get_course(uuid):
    try:
        course = Course.objects.get(id=uuid)
        return course
    except Course.DoesNotExist:
        return None


def get_class(uuid):
    try:
        current_class = Class.objects.get(id=uuid)
        return current_class
    except Class.DoesNotExist:
        return None


def get_subject(uuid):
    try:
        subject = Subject.objects.get(id=uuid)
        return subject
    except Subject.DoesNotExist:
        return None


def get_time_slot(uuid):
    try:
        time_slot = TimeSlot.objects.get(id=uuid)
        return time_slot
    except TimeSlot.DoesNotExist:
        return None


def get_assign(uuid):
    try:
        assign = Assign.objects.get(id=uuid)
        return assign
    except Assign.DoesNotExist:
        return None


def get_fee(uuid):
    try:
        fee = Fee.objects.get(id=uuid)
        return fee
    except Fee.DoesNotExist:
        return None


@administrator_message
@administrator_required
def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "administrator/home.html", context)


@administrator_message
@administrator_required
def create_academic_session_view(request, *args, **kwargs):
    context = {}
    form = AcademicSessionForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Academic Session created.")
            return redirect("administrator:academic-session-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Create"
    return render(request, "administrator/academic_session/academic_session_form.html", context)


@administrator_message
@administrator_required
def list_academic_session_view(request, *args, **kwargs):
    context = {}
    academic_sessions = AcademicSession.objects.all()
    context["academic_sessions"] = academic_sessions
    return render(request, "administrator/academic_session/academic_session_list.html", context)


@administrator_message
@administrator_required
def detail_academic_session_view(request, uuid, *args, **kwargs):
    context = {}
    academic_session = get_adademic_session(uuid)
    context["academic_session"] = academic_session
    return render(request, "administrator/academic_session/academic_session_detail.html", context)


@administrator_message
@administrator_required
def update_academic_session_view(request, uuid, *args, **kwargs):
    context = {}

    academic_session = get_adademic_session(uuid)
    form = AcademicSessionForm(request.POST or None, instance=academic_session)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Academic Session Updated.")
            return redirect("administrator:academic-session-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Update"
    return render(request, "administrator/academic_session/academic_session_form.html", context)


@administrator_message
@administrator_required
def delete_academic_session_view(request, uuid, *args, **kwargs):
    academic_session = get_adademic_session(uuid)

    if request.method == "POST":
        academic_session.delete()
        messages.success(request, f"Academic session has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:academic-session-list")


@administrator_message
@administrator_required
def create_department_view(request, *args, **kwargs):
    context = {}
    form = DepartmentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Department created.")
            return redirect("administrator:department-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Create"
    return render(request, "administrator/department/department_form.html", context)


@administrator_message
@administrator_required
def list_department_view(request, *args, **kwargs):
    context = {}
    departments = Department.objects.all()
    context["departments"] = departments
    return render(request, "administrator/department/department_list.html", context)


@administrator_message
@administrator_required
def detail_department_view(request, uuid, *args, **kwargs):
    context = {}
    department = get_department(uuid)
    context["department"] = department
    return render(request, "administrator/department/department_detail.html", context)


@administrator_message
@administrator_required
def update_department_view(request, uuid, *args, **kwargs):
    context = {}
    department = get_department(uuid)
    form = DepartmentForm(request.POST or None, instance=department)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Department Updated.")
            return redirect("administrator:department-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Update"
    return render(request, "administrator/department/department_form.html", context)


@administrator_message
@administrator_required
def delete_department_view(request, uuid, *args, **kwargs):
    department = get_department(uuid)

    if request.method == "POST":
        department.delete()
        messages.success(request, f"Department has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:department-list")


@administrator_message
@administrator_required
def create_course_view(request, *args, **kwargs):
    context = {}
    c_form = CourseForm(request.POST or None)
    f_form = FeeForm(request.POST or None)

    if request.method == "POST":
        if c_form.is_valid() and f_form.is_valid():
            course = c_form.save()
            fee = f_form.save(commit=False)
            fee.course = course
            fee.save()
            messages.success(request, f"Course created.")
            return redirect("administrator:course-list")
        else:
            c_form = c_form
            f_form = f_form
            messages.error(request, "Error.")

    context["c_form"] = c_form
    context["f_form"] = f_form
    context["action"] = "Create"
    return render(request, "administrator/course/course_form.html", context)


@administrator_message
@administrator_required
def list_course_view(request, *args, **kwargs):
    context = {}
    courses = Course.objects.all()
    context["courses"] = courses
    return render(request, "administrator/course/course_list.html", context)


@administrator_message
@administrator_required
def detail_course_view(request, uuid, *args, **kwargs):
    context = {}
    course = get_course(uuid)
    context["course"] = course
    return render(request, "administrator/course/course_detail.html", context)


@administrator_message
@administrator_required
def update_course_view(request, uuid, *args, **kwargs):
    context = {}
    course = get_course(uuid)
    if course:
        fee = Fee.objects.get(course=course)
    c_form = CourseForm(request.POST or None, instance=course)
    f_form = FeeForm(request.POST or None, instance=fee)

    if request.method == "POST":
        if c_form.is_valid() and f_form.is_valid():
            c_form.save()
            f_form.save()
            messages.success(request, f"Course Updated.")
            return redirect("administrator:course-list")
        else:
            c_form = c_form
            f_form = f_form
            messages.error(request, "Error.")

    context["c_form"] = c_form
    context["f_form"] = f_form
    context["action"] = "Update"
    return render(request, "administrator/course/course_form.html", context)


@administrator_message
@administrator_required
def delete_course_view(request, uuid, *args, **kwargs):
    course = get_course(uuid)

    if request.method == "POST":
        course.delete()
        messages.success(request, f"Course has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:course-list")


@administrator_message
@administrator_required
def create_class_view(request, *args, **kwargs):
    context = {}
    form = ClassForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Class created.")
            return redirect("administrator:class-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Create"
    return render(request, "administrator/class/class_form.html", context)


@administrator_message
@administrator_required
def list_class_view(request, *args, **kwargs):
    context = {}
    classes = Class.objects.all()
    context["classes"] = classes
    return render(request, "administrator/class/class_list.html", context)


@administrator_message
@administrator_required
def detail_class_view(request, uuid, *args, **kwargs):
    context = {}
    current_class = get_class(uuid)
    context["class"] = current_class
    return render(request, "administrator/class/class_detail.html", context)


@administrator_message
@administrator_required
def update_class_view(request, uuid, *args, **kwargs):
    context = {}
    current_class = get_class(uuid)
    form = ClassForm(request.POST or None, instance=current_class)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Class Updated.")
            return redirect("administrator:class-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Update"
    return render(request, "administrator/class/class_form.html", context)


@administrator_message
@administrator_required
def delete_class_view(request, uuid, *args, **kwargs):
    current_class = get_class(uuid)

    if request.method == "POST":
        current_class.delete()
        messages.success(request, f"Class has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:class-list")


@administrator_message
@administrator_required
def create_subject_view(request, *args, **kwargs):
    context = {}
    form = SubjectForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Subject created.")
            return redirect("administrator:subject-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Create"
    return render(request, "administrator/subject/subject_form.html", context)


@administrator_message
@administrator_required
def list_subject_view(request, *args, **kwargs):
    context = {}
    subjects = Subject.objects.all()
    context["subjects"] = subjects
    return render(request, "administrator/subject/subject_list.html", context)


@administrator_message
@administrator_required
def detail_subject_view(request, uuid, *args, **kwargs):
    context = {}
    subject = get_subject(uuid)
    context["subject"] = subject
    return render(request, "administrator/subject/subject_detail.html", context)


@administrator_message
@administrator_required
def update_subject_view(request, uuid, *args, **kwargs):
    context = {}
    subject = get_subject(uuid)
    form = SubjectForm(request.POST or None, instance=subject)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Subject Updated.")
            return redirect("administrator:subject-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Update"
    return render(request, "administrator/subject/subject_form.html", context)


@administrator_message
@administrator_required
def delete_subject_view(request, uuid, *args, **kwargs):
    subject = get_subject(uuid)

    if request.method == "POST":
        subject.delete()
        messages.success(request, f"Subject has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:subject-list")


@administrator_message
@administrator_required
def create_time_slot_view(request, *args, **kwargs):
    context = {}
    form = TimeSlotForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"TimeSlot created.")
            return redirect("administrator:time-slot-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Create"
    return render(request, "administrator/time_slot/time_slot_form.html", context)


@administrator_message
@administrator_required
def list_time_slot_view(request, *args, **kwargs):
    context = {}
    time_slots = TimeSlot.objects.all()
    context["time_slots"] = time_slots
    return render(request, "administrator/time_slot/time_slot_list.html", context)


@administrator_message
@administrator_required
def detail_time_slot_view(request, uuid, *args, **kwargs):
    context = {}
    time_slot = get_time_slot(uuid)
    context["time_slot"] = time_slot
    return render(request, "administrator/time_slot/time_slot_detail.html", context)


@administrator_message
@administrator_required
def update_time_slot_view(request, uuid, *args, **kwargs):
    context = {}
    time_slot = get_time_slot(uuid)
    form = TimeSlotForm(request.POST or None, instance=time_slot)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"TimeSlot Updated.")
            return redirect("administrator:time-slot-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Update"
    return render(request, "administrator/time_slot/time_slot_form.html", context)


@administrator_message
@administrator_required
def delete_time_slot_view(request, uuid, *args, **kwargs):
    time_slot = get_time_slot(uuid)

    if request.method == "POST":
        time_slot.delete()
        messages.success(request, f"TimeSlot has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:time-slot-list")


@administrator_message
@administrator_required
def create_assign_view(request, *args, **kwargs):
    context = {}
    form = AssignForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Assign created.")
            return redirect("administrator:assign-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Create"
    return render(request, "administrator/assign/assign_form.html", context)


@administrator_message
@administrator_required
def list_assign_view(request, *args, **kwargs):
    context = {}
    assigns = Assign.objects.all()
    context["assigns"] = assigns
    return render(request, "administrator/assign/assign_list.html", context)


@administrator_message
@administrator_required
def detail_assign_view(request, uuid, *args, **kwargs):
    context = {}
    assign = get_assign(uuid)
    context["assign"] = assign
    return render(request, "administrator/assign/assign_detail.html", context)


@administrator_message
@administrator_required
def update_assign_view(request, uuid, *args, **kwargs):
    context = {}
    assign = get_assign(uuid)
    form = AssignForm(request.POST or None, instance=assign)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Assign Updated.")
            return redirect("administrator:assign-list")
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["action"] = "Update"
    return render(request, "administrator/assign/assign_form.html", context)


@administrator_message
@administrator_required
def delete_assign_view(request, uuid, *args, **kwargs):
    assign = get_assign(uuid)

    if request.method == "POST":
        assign.delete()
        messages.success(request, f"Assign has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("administrator:assign-list")
