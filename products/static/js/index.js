
function quantityBtn (option, id) {
    const qty = document.getElementById(`${id}`);
    const value = Number(qty.value) 
    if (option === "decrease"){
        if ( value > 0){
            qty.value = value - 1
        }
    }
    else {
        qty.value = value + 1
    }
}