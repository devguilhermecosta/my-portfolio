from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path(
        'api/list/',  # get
        views.WorkListAPIV1View.as_view(),
        name='work-list',
    ),
    path(
        'api/create/',  # post
        views.WorkCreateDetailAPIV1View.as_view(),
        name='work-create',
    ),
    path(
        'api/<str:slug>/',  # get, patch and delete
        views.WorkCreateDetailAPIV1View.as_view(),
        name='work',
        ),
    path(
        'api/images/create/',  # post
        views.WorkImagesAPIView.as_view(),
        name='image-create',
        ),
    path(
        'api/image/<int:id>/',  # get, patch and delete
        views.WorkImagesAPIView.as_view(),
        name='image',
        ),
    path(
        'api/images/<int:id>/list/',  # get all images from a given job
        views.WorkImagesListAPIView.as_view(),
        name='image-list',
        ),
]
