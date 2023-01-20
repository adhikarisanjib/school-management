from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("base/", include("base.urls", namespace="base")),
    path("administrator/", include("administrator.urls", namespace="administrator")),
    path("accountant/", include("accountant.urls", namespace="accountant")),
    path("staff/", include("staff.urls", namespace="staff")),
    path("student/", include("student.urls", namespace="student")),
    path("conference/", include("conference.urls", namespace="conference")),
    path("", include("website.urls", namespace="website")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "base.views.page_not_found_view"
