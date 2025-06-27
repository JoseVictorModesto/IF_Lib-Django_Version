from apps.user_admin.models import Categoria, Tipos, Instituicao, Campus, Curso

# filtros do menu lateral
def menu_filtro(request):
    categorias = Categoria.objects.all()
    tipos = Tipos.objects.all()
    instituicoes = Instituicao.objects.all()
    campus = Campus.objects.all()
    cursos = Curso.objects.all()

    return {'categorias': categorias, 'tipos': tipos, 'instituicoes': instituicoes, 'campus': campus, 'cursos': cursos}