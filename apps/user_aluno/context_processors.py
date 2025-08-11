
def perfil_aluno_cp(request):
    if request.user.is_authenticated:
        user_aluno = getattr(request.user, 'usuario_aluno', None)
        return {'user_aluno':user_aluno}
    return{}