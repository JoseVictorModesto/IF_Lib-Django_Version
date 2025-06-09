from django.urls import path
from apps.login_perfil.views import login, logout

# urls home
urlpatterns = [
        path('login/', login, name='login'),
        path('logout/', logout, name='logout'),
]