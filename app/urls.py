from django.contrib import admin
from django.urls import path, include
from .views import UploadViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("upload", UploadViewSet, basename="Upload")

urlpatterns = [
    path("", include(router.urls)),
    # taxes
    path(
        "upload",
        UploadViewSet.as_view(
            {
                "post": "upload",
            }
        ),
    ),
]
