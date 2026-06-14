var days_needed = document.getElementById('days_needed');

function hide_btn(){
    let button = document.getElementById('hide_btn');
    button.addEventListener('click', hide_hero);
}

function hide_hero(){
    let hero = document.getElementById('hero-fullheight');
    hero.style.display = 'none';
}

function populate_recipe(){

}



document.addEventListener('DOMContentLoaded', hide_btn);
document.addEventListener('DOMContentLoaded', populate_recipe);
