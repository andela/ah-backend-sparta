from django.urls import include, path
from django.contrib import admin

app_name = "Authors' Haven"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('authors.apps.authentication.urls')),
]

