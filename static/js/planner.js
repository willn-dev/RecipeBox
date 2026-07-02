function hide_btn(){
    let button = document.getElementById('hide_btn');
    button.addEventListener('click', hide_hero);

    let listholder = document.getElementById('listHolder');
    listholder.addEventListener('click', reroller); // this is to allow items to be reloaded later

}


function hide_hero(){

    var days_needed_raw = document.getElementById('days_needed');
    var days_needed = parseInt(days_needed_raw.value);


    let hero = document.getElementById('hero-fullheight');
    hero.style.display = 'none';
    populate_plan(days_needed);
}

var recipes_loaded = [];
var recipes_excluded = [];

function populate_plan(days){
    console.log(recipe_pool[1]);
    let listholder = document.getElementById('listHolder');

    for(let i = 0; i < days; i++){
        recipe = document.createElement('li');
        recipe.classList.add('list-row');

        recipe.innerHTML = `
            <div id="name" class="text-2xl justify-self-center">${recipe_pool[i][0]}</div>
            <div></div>
            <button id="${recipe_pool[i][1]}" class="btn btn-square btn-ghost mr-10">
            <svg class="size-[1.2em] text-accent fill-accent" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="30" height="30" viewBox="0 0 30 30">
            <path d="M 15 3 C 12.031398 3 9.3028202 4.0834384 7.2070312 5.875 A 1.0001 1.0001 0 1 0 8.5058594 7.3945312 C 10.25407 5.9000929 12.516602 5 15 5 C 20.19656 5 24.450989 8.9379267 24.951172 14 L 22 14 L 26 20 L 30 14 L 26.949219 14 C 26.437925 7.8516588 21.277839 3 15 3 z M 4 10 L 0 16 L 3.0507812 16 C 3.562075 22.148341 8.7221607 27 15 27 C 17.968602 27 20.69718 25.916562 22.792969 24.125 A 1.0001 1.0001 0 1 0 21.494141 22.605469 C 19.74593 24.099907 17.483398 25 15 25 C 9.80344 25 5.5490109 21.062074 5.0488281 16 L 8 16 L 4 10 z"></path>
            </svg>
            </button>
            <input type="checkbox" checked="checked" class="checkbox mr-5 mt-2" name="needInstructions" value="${recipe_pool[i][1]}"/>
        `;

        listholder.append(recipe);
        recipes_loaded.push(recipe_pool[i][1]);

    }
}

function reroller(evt){
    let button = evt.target.closest('button');

    if (button){
        let btn_id = Number(button.id);
        let row = button.closest('li');
        let name_div = row.querySelector('#name');

        toAdd = recipe_pool.find(recipe_pair => !recipes_loaded.includes(recipe_pair[1]) && !recipes_excluded.includes(recipe_pair[1])); //recipe_pair is name given to each element in recipe_pool as it iterates.

        if (toAdd){
            recipes_excluded.push(btn_id);
            recipes_loaded = recipes_loaded.filter(num => num !== btn_id);
            button.id = toAdd[1];
                name_div.innerHTML = `${toAdd[0]}`;
                recipes_loaded.push(toAdd[1]);
                console.log(recipes_loaded);
        }
        else{

            button.id = null;
            name_div.innerHTML = `Theres no more recipes to add!!`;
        }
    }
}


function passArray(){
    let form = document.getElementById('plan-form');
    form.addEventListener('submit', passInputToHidden);

    function passInputToHidden(){
    
      let checkbox_values = document.querySelectorAll('input[name="needInstructions"]:checked');
      let checkbox_arr = [...checkbox_values].map(cb => parseInt(cb.value));
      console.log(checkbox_arr);

      let hiddenInput = document.getElementById('js-pass-array');
      hiddenInput.value = `${JSON.stringify(recipes_loaded)}`;

      let recipe_needed = document.getElementById('checkbox_value');
      recipe_needed.value = `${JSON.stringify(checkbox_arr)}`;

    }
}

document.addEventListener('DOMContentLoaded', hide_btn);
document.addEventListener('DOMContentLoaded', passArray)
