from django.urls import path
from . import views


app_name = 'networks'


urlpatterns = [
    path('api/v1/',
         views.NetworksApiV1View.as_view(),
         name='networks',
         ),
]
