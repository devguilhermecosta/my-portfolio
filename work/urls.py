from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path(
        'list/',
        views.WorkListAPIV1View.as_view(),
        name='work-list',
    ),
    path(
        'create/',
        views.WorkCreateDetailAPIV1View.as_view(),
        name='work-create',
    ),
    path(
        '<str:slug>/',
        views.WorkCreateDetailAPIV1View.as_view(),
        name='work-detail',
        ),
    path(
        '<int:id>/images/',
        views.WorkImagesAPIView.as_view(),
        name='images-work',
        ),
]
