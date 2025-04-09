document.addEventListener("DOMContentLoaded", function () {
    // استفاده از event delegation برای دکمه‌های جدید
    document.body.addEventListener("click", function (e) {
        if (e.target && e.target.matches(".add-to-cart")) {
            e.preventDefault();
            let productId = e.target.dataset.productId;

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
                    e.target.nextElementSibling.style.display = "inline";  // نمایش لینک مشاهده سبد خرید
                });
        }
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
