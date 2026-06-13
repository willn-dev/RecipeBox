var days_needed = document.getElementById('days_needed');

function hide_btn(){
    let button = document.getElementById('hide_btn');
    button.addEventListener('click', hide_hero);
}

function hide_hero(){
    let hero = document.getElementById('hero-fullheight');
    hero.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', hide_btn);