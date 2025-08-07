
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
    const getPrice = document.getElementById(`${price}`);
    const getQuantity = document.getElementById(`${quantity}`);
    const getTotal = document.getElementById(`${total}`);
    const getInputValue = document.getElementById(`${inputValue}`);
    const getCarttValue = document.getElementById(`${cartTotalValue}`);


    let cartTotal = 0
    if (Number(getQuantity.innerText) >= 1){
        if (action == "-" && Number(getQuantity.innerText) > 1){
            getQuantity.innerText = Number(getQuantity.innerText) - 1 
        }
        else if(action == "+"){
            getQuantity.innerText = Number(getQuantity.innerText) + 1
         }

        const new_price = Number(getPrice.innerText)
        const new_quantity = Number(getQuantity.innerText)
        getTotal.innerText = new_price * new_quantity
        getInputValue.value = new_quantity
        console.log("GET QUANTITY", getInputValue)
    }


    const totalList = document.querySelectorAll(`.${getItemTotal}`)
    totalList.forEach((total) => {
        cartTotal += Number(total.innerText)
    })
    const setCartTotal = document.getElementById(`${getCartTotal}`) 
    setCartTotal.innerText = cartTotal
    getCarttValue.value = cartTotal
    console.log("GET INPUT TOTAL", getCarttValue.value)


}




// let ourService = document.querySelector(".our-services")
// let hiddenServices = document.querySelectorAll(".our-service-hidden")
// let container = document.querySelector(".hide-our-service")

// ourService.addEventListener("mouseover", ()=> {

//         hiddenServices.forEach((elem) => {
//             elem.classList.add("our-services-visible")
//         })

//         container.classList.add("display-our-service")
//         console.log("Add class")

// })

// ourService.addEventListener("mouseout", ()=> {

//         hiddenServices.forEach((elem) => {
//             elem.classList.remove("our-services-visible")
//         })
//         container.classList.remove("display-our-service")

//         console.log("Remove class")
// })

//   window.addEventListener("load", () => {
//     const fontAwesomeElement = document.createElement("i");
//     fontAwesomeElement.className = "fa fa-solid";
//     document.body.appendChild(fontAwesomeElement);
//     const style = window.getComputedStyle(fontAwesomeElement, "::before").content;
//     document.body.removeChild(fontAwesomeElement);

//     if (!style || style === "none" || style === '""') {
//       document.querySelectorAll(".fa").forEach(el => {
//         el.textContent = el.getAttribute("alt") || "Icon";
//       });
//     }
//   });


// document.getElementById("copyright").innerHTML = <i class="fa-solid fa-copyright">lizzy-hairapy</i> + ` ${Date.now()}`;


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


// Hide dropdown if user clicks outside
// document.addEventListener("click", () => {
  
//   }
// });

// Optional: Hide when user clicks a dropdown item
const items = document.querySelectorAll(".our-service-dropdown div");
items.forEach((item) => {
  item.addEventListener("click", () => {
    hiddenServices.classList.remove("our-services-visible");
  });
});



