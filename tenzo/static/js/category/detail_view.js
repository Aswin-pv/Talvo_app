// increase quantity
document.getElementById('decrease').addEventListener('click',()=>{
    var quantityInput = document.getElementById('quantity');
    var currentValue = parseInt(quantityInput.value);

    if (currentValue > 1) {
         quantityInput.value = currentValue - 1;
    }
});

//decrease quantity
document.getElementById('increase').addEventListener('click',()=>{
    var quantityInput = document.getElementById('quantity');
    var currentValue = parseInt(quantityInput.value);   
    quantityInput.value = currentValue + 1;
});



