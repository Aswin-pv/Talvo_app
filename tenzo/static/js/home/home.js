document.getElementById("SignupRedirect").addEventListener('click',()=>{
    window.location.href = "{% url 'register' %}"
})