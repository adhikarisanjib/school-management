from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render

from base.forms import LoginForm
from base.views import get_login_type
from school.tasks import send_user_activation_email


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "website/home.html", context)


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

            # if not user.is_email_verified:
            #     site = get_current_site(request)
            #     domain = site.domain
            #     if settings.CELERY_SERVER_RUNNING:
            #         send_user_activation_email.delay(user.id, domain)
            #     else:
            #         send_user_activation_email(user.id, domain)
            #     messages.success(
            #         request,
            #         f"An email with verification link is sent to your Email ID. Verify Your account before login.",
            #     )
            #     return redirect("website:home")

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
                    return redirect("website:home")

        else:
            messages.error(request, f"Invalid email or password.")

    context["form"] = form
    return render(request, "website/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("website:home")
