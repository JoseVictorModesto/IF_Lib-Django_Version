from django.urls import path
from apps.home.views import index

# urls home
urlpatterns = [
    path('', index, name='home'),
]