
function printout(){
    window.print();
    window.onafterprint = () => {window.location.href = '/';};
    
}

document.addEventListener('DOMContentLoaded', printout);