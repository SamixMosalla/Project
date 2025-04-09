document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart").forEach(function (button) {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            let productId = this.dataset.productId;

            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `product_id=${productId}`
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("cart-total-items").innerText = data.total_items;
                    document.getElementById("cart-total-price").innerText = data.total_price + " تومان";
                    this.nextElementSibling.style.display = "inline";
                });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
