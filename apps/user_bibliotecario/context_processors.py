def perfil_bibliotecario_cp(request):
    if request.user.is_authenticated:
        user_bibliotecario = getattr(request.user, 'usuario_bibliotecario', None)
        return {'user_bibliotecario':user_bibliotecario}
    return{}
