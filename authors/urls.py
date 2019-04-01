from django.urls import include, path
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Authors' Haven")

app_name = "Authors' Haven"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger-docs/', schema_view),
    path('api/', include('authors.apps.authentication.urls')),
]

