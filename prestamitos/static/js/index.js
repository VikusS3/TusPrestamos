document.addEventListener('DOMContentLoaded', function(){
    const menuButton = document.querySelector('.menu-button')
    const nav = document.querySelector('nav')


    menuButton.addEventListener('click', ()=>{
        nav.classList.toggle('show');
    })

    //hacer rotar al boton de menu
    menuButton.addEventListener('click', ()=>{
        menuButton.classList.toggle('rotate');
    })
})


