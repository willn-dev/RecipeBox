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

//need to use json_pool const
//also need to take note of the amount selected on slider with days_needed
//solve when refresh selects new from pool.

document.addEventListener('DOMContentLoaded', hide_btn);
document.addEventListener('DOMContentLoaded', populate_recipe);
