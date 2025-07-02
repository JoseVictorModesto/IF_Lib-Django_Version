from apps.user_admin.models import Categoria, Tipos, Instituicao, Campus, Curso
from django.views.decorators.http import require_GET

# filtros do menu lateral
@require_GET
def menu_filtro(request):
    categorias = Categoria.objects.order_by('nome_categoria')
    tipos = Tipos.objects.order_by('nome_tipo')
    instituicoes = Instituicao.objects.order_by('nome_instituicao')
    campus = Campus.objects.order_by('nome_campus')
    cursos = Curso.objects.order_by('nome_curso')

    return {'categorias': categorias, 'tipos': tipos, 'instituicoes': instituicoes, 'campus': campus, 'cursos': cursos}