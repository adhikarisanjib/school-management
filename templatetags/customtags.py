from django import template

register = template.Library()


@register.filter
def isLineInput(value):
    return value.field.widget.input_type in [
        "date",
        "datetime-local",
        "email",
        "file",
        "image",
        "number",
        "password",
        "range",
        "tel",
        "text",
        "url",
    ]


@register.filter
def isPointInput(value):
    return value.field.widget.input_type in [
        "checkbox",
        "radio",
    ]


@register.filter
def splitFieldName(value):
    field_name = str(value).split(".")[-1]
    field_name = field_name.replace("_", " ")
    return field_name


@register.filter
def removeUnderscore(value, arg):
    return value.replace(arg, " ")


@register.filter
def addUnderscore(value, arg):
    return value.replace(" ", arg)
