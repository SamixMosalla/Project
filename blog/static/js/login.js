document.getElementById("toggleBtn").addEventListener("click", function () {
    let button = this
    let registerform = document.getElementById("form-register")
    let loginform = document.getElementById('form-login')
    if (button.innerText == 'ورود') {
        button.innerText = 'ثبت نام'
        registerform.style.display = "none"
        loginform.style.display = "block"
    } else {
        button.innerText = 'ورود'
        registerform.style.display = "block"
        loginform.style.display = "none"
    }
})