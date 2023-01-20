from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.handlers.wsgi import WSGIRequest


def administrator_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.user_type.name == "administrator",
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def administrator_message(function):
    def message_function(request, uuid=None, *args, **kwargs):
        if isinstance(request, WSGIRequest):
            if request.user.is_authenticated and not request.user.user_type.name == "administrator":
                messages.error(request, "You must login as administrator to access this page.")
            elif not request.user.is_authenticated:
                messages.error(request, "You must login to access this page.")
        return function(request, uuid, *args, **kwargs)

    return message_function
