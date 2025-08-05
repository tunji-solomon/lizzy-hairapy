
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

function totalCost (price, quantity, total, action, getItemTotal, getCartTotal) {
    const getPrice = document.getElementById(`${price}`);
    const getQuantity = document.getElementById(`${quantity}`);
    const getTotal = document.getElementById(`${total}`);
    let cartTotal = 0

    if (getQuantity.innerText >= 0){
        if (action == "-" && getQuantity.innerText > 0){
            getQuantity.innerText = Number(getQuantity.innerText) - 1 
        }
        else if(action == "+"){
            getQuantity.innerText = Number(getQuantity.innerText) + 1
         }

        const new_price = Number(getPrice.innerText)
        const new_quantity = Number(getQuantity.innerText)
        getTotal.innerText = new_price * new_quantity
    }

    const totalList = document.querySelectorAll(`.${getItemTotal}`)
    totalList.forEach((total) => {
        cartTotal += Number(total.innerText)
    })
    const setCartTotal = document.getElementById(`${getCartTotal}`) 
    setCartTotal.innerText = cartTotal


}




