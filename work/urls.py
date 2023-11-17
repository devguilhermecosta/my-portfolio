from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path(
        '<int:id>/images/',
        views.WorkImagesAPIView.as_view(),
        name='images-work',
        ),
    path(
        '<str:slug>/',
        views.WorkAPIV1View.as_view(),
        name='work',
        ),
]
