from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, re_path
from django.views.static import serve

from core.settings import ENVIRONMENT, MEDIA_ROOT, STATIC_ROOT


def home_view(request):
    return redirect("accounts:cross-auth")


def handler404(request, *args, **kwargs):
    return render(request, "404.html")


def handler500(request, *args, **kwargs):
    return render(request, "500.html")


# EXTERNAL APPS URLS
urlpatterns = [

    # DJANGO URLS > remove in extreme security
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
]

# your apps urls
urlpatterns += [
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('admins/', include('src.administration.admins.urls', namespace='admins')),
    path('staff/', include('src.administration.staff.urls', namespace='staff')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

# if ENVIRONMENT != 'server':
#     urlpatterns += [
#         path("__reload__/", include("django_browser_reload.urls")),
#     ]
