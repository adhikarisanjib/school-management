from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomFileInput(ClearableFileInput):
    template_name = "base/widgets/clearable_file_input.html"
