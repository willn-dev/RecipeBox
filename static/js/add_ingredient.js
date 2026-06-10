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
    <input name="ingredient_name" type="text" required class="input input-lg input-accent w-full text-lg font-mono">
    <input placeholder="Qty." type="text" name="ingredient_qty" class="input validator input-lg input-accent text-lg font-mono w-1/4"> 
    `;

    newRow.classList.add('mt-2'); 
    
    ingredientContainer.insertBefore(newRow, button);
}


function del_button(){
    let button = document.querySelector('#delete');
    button.addEventListener('click', confirm_and_submit);
}

async function confirm_and_submit(){
    let isDeleteOK = confirm('Are you sure you want to delete this? You wont be able to recover it.');
    
    if(isDeleteOK){
        var recipe_id = document.querySelector('#recipe_id').value;
        if(!recipe_id) return;
        let response = await fetch("/delete", {
            method: 'POST',
            body: JSON.stringify({
                id: recipe_id
            }),
            headers:{
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        let final_reply = await response.json();
        console.log(final_reply.redirect, final_reply.status)

            window.location = final_reply.redirect
    }
}

document.addEventListener('DOMContentLoaded', button_listen);
document.addEventListener('DOMContentLoaded', del_button);