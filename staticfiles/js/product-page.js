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
                    this.nextElementSibling.style.display = "inline";  // نمایش لینک "مشاهده سبد خرید"
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













// product image 
    const container = document.querySelector(".container-product-img");
    const img = container.querySelector(".product-image");

    container.addEventListener("mousemove", (e) => {
        let { left, top, width, height } = container.getBoundingClientRect();
        let x = ((e.clientX - left) / width) * 100;
        let y = ((e.clientY - top) / height) * 100;

        img.style.transformOrigin = `${x}% ${y}%`;
        img.style.transform = "scale(2)";
    });

    container.addEventListener("mouseleave", () => {
        img.style.transform = "scale(1)";
        img.style.transformOrigin = "center";
    });