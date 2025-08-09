
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

function totalCost (price, quantity, total, action, getItemTotal, getCartTotal, inputValue, cartTotalValue) {
    let getPrice = document.getElementById(`${price}`);
    const getQuantity = document.getElementById(`${quantity}`);
    const getTotal = document.getElementById(`${total}`);
    const getInputValue = document.getElementById(`${inputValue}`);
    const getCarttValue = document.getElementById(`${cartTotalValue}`);

    getPrice = getPrice.innerText.replace(",","")
    console.log(getPrice)
    let cartTotal = 0
    if (Number(getQuantity.innerText) >= 1){
        if (action == "-" && Number(getQuantity.innerText) > 1){
            getQuantity.innerText = Number(getQuantity.innerText) - 1 
        }
        else if(action == "+"){
            getQuantity.innerText = Number(getQuantity.innerText) + 1
         }

        const new_price = Number(getPrice)
        const new_quantity = Number(getQuantity.innerText)
        getTotal.innerText = formatPrice(new_price * new_quantity)

        getInputValue.value = new_quantity
    }


    const totalList = document.querySelectorAll(`.${getItemTotal}`)
    totalList.forEach((total) => {
        cartTotal += Number(total.innerText.replace(/,/g, ""))
    })
    const setCartTotal = document.getElementById(`${getCartTotal}`) 
    setCartTotal.innerText = formatPrice(cartTotal)
    getCarttValue.value = cartTotal


}

function formatPrice(value) {
    // value = String(value)
    // if (value.length == 4) {
    //     value = value[0] + ',' + value.slice(1)
    // }else{
    //     if (value.length == 5) {
    //         value = value.slice(0,2) + "," + value.slice(2)
    //     }else{
    //         if (value.length == 6 ){
    //         value = value.slice(0,3) + "," + value.slice(3)
    //         }else {
    //             if (value.length == 7){
    //                 value = value[0] + ',' + value.slice(1, 4) + ',' + value.slice(4)
    //             }else {
    //                 if (value.length == 8){
    //                     value = value.slice(0,2) + ',' + value.slice(2, 5) + ',' + value.slice(5)

    //                 }else {
    //                     if (value.length == 9){
    //                                 value = value.slice(0,3) + ',' + value.slice(3, 6) + ',' + value.slice(6)
    //                     }
    //                 }                      
    //             }
    //         }
    //     }
        
    // }
    return Number(value.toString().replace(/,/g, "")).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}



const ourService = document.querySelector(".our-services");
const hiddenServices = document.querySelector(".our-service-dropdown");

ourService.addEventListener("mouseover", myHandler);
ourService.addEventListener("click", myHandler);
ourService.addEventListener("mouseout", myHandler);

function myHandler(e) {
    if(["mouseover"].includes(e.type)){
        e.stopPropagation()
        hiddenServices.classList.add("our-services-visible");
 
    }else if(e.type == "click"){
        hiddenServices.classList.remove("our-services-visible")
    }
    else{
        hiddenServices.classList.remove("our-services-visible");
    }
}


// Hide when user clicks a dropdown item
const items = document.querySelectorAll(".our-service-dropdown div");
items.forEach((item) => {
  item.addEventListener("click", () => {
    hiddenServices.classList.remove("our-services-visible");
  });
});


function confirmAction(container, action){
    const modalContainer = document.querySelector(`.${container}`);

    if (action != "cancel"){
        modalContainer.classList.add("modal-visible")
    }else{
        modalContainer.classList.remove("modal-visible")
    }
    


    // ourService.addEventListener("mouseover", myHandler);
    // ourService.addEventListener("click", myHandler);
    // ourService.addEventListener("mouseout", myHandler);

    // function myHandler(e) {
    //     if(["mouseover"].includes(e.type)){
    //         e.stopPropagation()
    //         hiddenServices.classList.add("our-services-visible");
    
    //     }else if(e.type == "click"){
    //         hiddenServices.classList.remove("our-services-visible")
    //     }
    //     else{
    //         hiddenServices.classList.remove("our-services-visible");
    //     }
    // }
}



