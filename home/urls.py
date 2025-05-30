from django.urls import path
from home.views import index

# urls home
urlpatterns = [
    path('', index, name='home'),
]