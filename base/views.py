from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from base.forms import (
    LoginForm,
    PasswordChangeForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    RegistrationForm,
    UserUpdateForm,
)
from base.models import User
from base.tokens import account_activation_token
from school.tasks import send_password_reset_email, send_user_activation_email


def get_login_type(user):
    try:
        return user.user_type.name
    except Exception as e:
        return ""


@login_required
def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "base/home.html", context)


def login_view(request, *args, **kwargs):
    context = {}

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)

            if not user.is_active:
                user.is_active = True

            if not user.is_email_verified:
                site = get_current_site(request)
                domain = site.domain
                if settings.CELERY_SERVER_RUNNING:
                    send_user_activation_email.delay(user.id, domain)
                else:
                    send_user_activation_email(user.id, domain)
                messages.success(
                    request,
                    f"An email with verification link is sent to your Email ID. Verify Your account before login.",
                )
                return redirect("base:home")

            login(request, user)
            messages.success(request, "Login Successfull.")
            redirect_url = request.POST.get("next", None)
            if redirect_url:
                return redirect(redirect_url)

            login_type = get_login_type(user)
            match login_type:
                case "administrator":
                    return redirect("administrator:home")
                case "accountant":
                    return redirect("accountant:home")
                case "teacher":
                    return redirect("staff:home")
                case "student":
                    return redirect("student:home")
                case other:
                    return redirect("base:home")

        else:
            messages.error(request, f"Invalid email or password.")

    context["form"] = form
    return render(request, "base/login.html", context)


def register_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        messages.info(request, "You are already registered.")
        return redirect("base:home")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()

            user.username = user.email.split("@")[0]
            user.save()

            site = get_current_site(request)
            domain = site.domain
            if settings.CELERY_SERVER_RUNNING:
                send_user_activation_email.delay(user.id, domain)
            else:
                send_user_activation_email(user.id, domain)
            messages.success(
                request,
                f"An email with verification link is sent to your Email ID. Verify Your account before login.",
            )

            return redirect("base:login")

        else:
            messages.error(request, f"Error in data validation.")

    context["form"] = form
    return render(request, "base/register.html", context)


def logout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("base:login")


@login_required
def user_profile_view(request, *args, **kwargs):
    context = {}

    user_id = kwargs.get("user_id", None)
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User not found.")
    else:
        user = request.user

    context["user"] = user
    return render(request, "base/user-profile.html", context)


@login_required
def user_update_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if request.method == "GET":
        form = UserUpdateForm(instance=user)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("base:user-profile")
        else:
            messages.error(request, f"Error...")

    context["form"] = form
    return render(request, "base/user-update.html", context)


@login_required
def user_deactivate_view(request, *args, **kwargs):
    user = request.user

    if request.method == "POST":
        user.is_active = False
        logout(request)
        messages.success(request, f"Your account has been deactivated. Login anytime to reactivate it.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("base:home")


@login_required
def user_delete_view(request, *args, **kwargs):
    user = request.user

    if request.method == "POST":
        user.delete()
        messages.success(request, f"Your account has been deleted successfully.")
    else:
        messages.error(request, "Something went wrong.")
    return redirect("base:home")


def email_verify_view(request, uidb64, token, *args, **kwargs):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        login(request, user)
        messages.success(request, f"An account for {user.username} created successfully.")
        return redirect("base:home")
    else:
        messages.error(request, f"Something went wrong.")
        return redirect("base:home")


@login_required
def password_change_view(request, *args, **kwargs):
    context = {}

    user = request.user
    form = PasswordChangeForm(user, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Password changed successfully. Please login with new password to continue.",
            )
        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["header"] = "Change Password"
    context["button_text"] = "Change"
    return render(request, "base/password/password-form.html", context)


def password_reset_request_view(request, *args, **kwargs):
    context = {}

    form = PasswordResetRequestForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = request.POST["email"]

            site = get_current_site(request)
            domain = site.domain
            if settings.CELERY_SERVER_RUNNING:
                send_password_reset_email.delay(email, domain)
            else:
                send_password_reset_email(email, domain)
            messages.success(
                request,
                f"An email with password reset link is sent to your Email ID. Verify Your account before login.",
            )

        else:
            form = form
            messages.error(request, "Error.")

    context["form"] = form
    context["header"] = "Request Password Reset"
    context["button_text"] = "Request"
    return render(request, "base/password/password-form.html", context)


def password_reset_view(request, uidb64, token, *args, **kwargs):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {}

    if user is not None and account_activation_token.check_token(user, token):
        form = PasswordResetForm(user, request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    f"Your password has been reset. Please login to continue.",
                )
                return redirect("base:login")
            else:
                form = form
            messages.error(request, "Error.")

        context["form"] = form
        context["header"] = "Request Password Reset"
        context["button_text"] = "Change"
        return render(request, "base/password/password-form.html", context)
    else:
        messages.info(request, f"Something went wrong.")
        return redirect("base:home")


def page_not_found_view(request, *args, **kwargs):
    return render(request, "base/page-not-found.html")
