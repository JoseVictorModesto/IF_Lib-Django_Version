function abrirInforCards(){
    document.querySelectorAll('.card').forEach(card => {
        const exiDescricao = card.querySelector('.descricao_card');
        const fecDescricao = card.querySelector('.retornar_card');
        const exidetalhes = card.querySelector('.detalhes_card');

        exiDescricao.addEventListener('click', () => {
            exidetalhes.classList.add('abrir');
        });

        fecDescricao.addEventListener('click', () => {
            exidetalhes.classList.remove('abrir');
        });
    });
};

function OpcoesMenuLateral() {
    const filtrosMenuLateral = document.querySelectorAll('.opcao_menu_lateral');

    filtrosMenuLateral.forEach(opcaoFiltro => {
        opcaoFiltro.addEventListener('click', function() {

            const filtrosMenu = this.querySelector('.filtros_menu_lateral');

                filtrosMenu.classList.toggle('mostrar_filtro');
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    abrirInforCards();
    OpcoesMenuLateral();
});