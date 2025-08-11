from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# urls gerais
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('login_perfil/', include("apps.login_perfil.urls")),
    path('user_admin/', include("apps.user_admin.urls")),
    path('user_bibliotecario/', include("apps.user_bibliotecario.urls")),
    path('user_professor/', include("apps.user_professor.urls")),
    path('user_aluno/', include("apps.user_aluno.urls")),
    path('filtros_buscas/', include("apps.filtros_buscas.urls")),
    path('notificacao/', include("apps.notificacao.urls")),
    path('conteudos/', include("apps.conteudos.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
