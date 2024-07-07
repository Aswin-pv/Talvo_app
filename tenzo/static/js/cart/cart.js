// increase quantity
document.querySelectorAll('.increase-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        let quantityInput = this.parentNode.querySelector('.input-qty');
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
});

// decrease quantity
document.querySelectorAll('.decrease-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        let quantityInput = this.parentNode.querySelector('.input-qty');
        let currentValue = parseInt(quantityInput.value); 
     
        quantityInput.value = currentValue - 1;
       
     
        
            
    });
});
