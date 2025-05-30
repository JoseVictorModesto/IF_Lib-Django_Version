from django.shortcuts import render

# Função exibição do index
def index(request):
    return render(request, 'main/index.html')
