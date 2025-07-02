def perfil_professor_cp(request):
    if request.user.is_authenticated:
        user_professor = getattr(request.user, 'usuario_professor', None)
        return {'user_professor':user_professor}
    return{}