

function hide_btn(){
    let button = document.getElementById('hide_btn');
    button.addEventListener('click', hide_hero);
}

function hide_hero(){
    let days_needed_raw = document.getElementById('days_needed');
    var days_needed = parseInt(days_needed_raw.value);

    let hero = document.getElementById('hero-fullheight');
    hero.style.display = 'none';
    populate_plan(days_needed);
}

function populate_plan(days){
    console.log(recipe_pool[1]);
    let listholder = document.getElementById('listHolder');
    var recipes_loaded = [];

    for(let i = 0; i < days - 1; i++){
        recipe = document.createElement('li');
        recipe.classList.add('list-row');

        recipe.innerHTML = `
            <div id="name" class="text-2xl justify-self-center">${recipe_pool[i][0]}</div>
            <button id="${recipe_pool[i][1]}" class="btn btn-square btn-ghost">
            <svg class="size-[1.2em] text-accent fill-accent" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="30" height="30" viewBox="0 0 30 30">
            <path d="M 15 3 C 12.031398 3 9.3028202 4.0834384 7.2070312 5.875 A 1.0001 1.0001 0 1 0 8.5058594 7.3945312 C 10.25407 5.9000929 12.516602 5 15 5 C 20.19656 5 24.450989 8.9379267 24.951172 14 L 22 14 L 26 20 L 30 14 L 26.949219 14 C 26.437925 7.8516588 21.277839 3 15 3 z M 4 10 L 0 16 L 3.0507812 16 C 3.562075 22.148341 8.7221607 27 15 27 C 17.968602 27 20.69718 25.916562 22.792969 24.125 A 1.0001 1.0001 0 1 0 21.494141 22.605469 C 19.74593 24.099907 17.483398 25 15 25 C 9.80344 25 5.5490109 21.062074 5.0488281 16 L 8 16 L 4 10 z"></path>
            </svg>
            </button>
        `;

        listholder.append(recipe);
        recipes_loaded.push(recipe_pool[i][1]);

    }
}
//solve when refresh selects new from pool.

document.addEventListener('DOMContentLoaded', hide_btn);
