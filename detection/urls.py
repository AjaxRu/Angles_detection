from django.urls import path
from .views import ImageDetectionView

urlpatterns = [
    path('detect/',
         ImageDetectionView.as_view(),
         name='image-detection'),
]
