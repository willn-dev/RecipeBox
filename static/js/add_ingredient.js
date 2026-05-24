// for adding another input field to the ingredients list.

function button_listen(){
    let button = document.querySelector('#add-new-btn');

    button.addEventListener('click', addIngredient);
}

function addIngredient(){
    let ingredientContainer = document.querySelector('#ingredient-col');
    let button = document.querySelector('#add-new-btn');
    let newRow = document.createElement('div');

    newRow.classList.add('flex', 'flex-row', 'gap-1', 'items-center', 'relative');

    newRow.innerHTML = `
    <button class="btn md:btn-xs btn-ghost align-center absolute -left-11 md:-left-6" id="removeIngredient" onclick="this.parentElement.remove()">&times;</button>
    <input name = "ingedient_name" type="text" required class= "input input-lg input-accent w-full text-lg font-mono">
    <input placeholder="Qty." type="number" name="ingredient_qty" class="input validator input-lg input-accent text-lg font-mono w-1/4"> 
    `;

    newRow.classList.add('mt-2'); 
    
    ingredientContainer.insertBefore(newRow, button);
    count_ingredients++;

}

document.addEventListener('DOMContentLoaded', button_listen);