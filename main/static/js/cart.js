document.addEventListener("DOMContentLoaded", function () {
    function updateCart(action, productId, quantity = null) {
        let data = `action=${action}&product_id=${productId}`;
        if (quantity !== null) {
            data += `&quantity=${quantity}`;
        }

        fetch("/update-cart/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: data
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartTotals(data);
                    if (action === "remove") {
                        document.querySelector(`tbody[data-product-id="${productId}"]`).remove();
                    } else {
                        updateProductRow(data.cart[productId], productId);
                    }
                }
            });
    }

    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.closest("tbody").dataset.productId;
            updateCart("remove", productId);
        });
    });


    //  add count product with + 
    document.querySelectorAll(".increase-qty").forEach(button => {
        button.addEventListener("click", function () {
            let row = this.closest("tbody");
            let productId = row.dataset.productId;
            let qtyInput = row.querySelector(".qty-input");
            let newQuantity = parseInt(qtyInput.value) + 1;
            qtyInput.value = newQuantity;
            updateCart("update", productId, newQuantity);
        });
    });

    // minus products with - 
    document.querySelectorAll(".decrease-qty").forEach(button => {
        button.addEventListener("click", function () {
            let row = this.closest("tbody");
            let productId = row.dataset.productId;
            let qtyInput = row.querySelector(".qty-input");
            let newQuantity = Math.max(1, parseInt(qtyInput.value) - 1);
            qtyInput.value = newQuantity;
            updateCart("update", productId, newQuantity);
        });
    });

    // update count and price 
    function updateCartTotals(data) {
        document.getElementById("cart-total-items").innerText = data.total_items;
        document.getElementById("cart-total-price").innerText = `${data.total_price} تومان`;
        document.getElementById('total-price-update').innerText = `${data.total_price} تومان`
        document.getElementById('sum-total-price').innerText = `${data.total_price} تومان`
    }

    // آپدیت قیمت کل هر محصول
    function updateProductRow(product, productId) {
        let row = document.querySelector(`tbody[data-product-id="${productId}"]`);
        row.querySelector(".td-total-price").innerText = `${product.total_price} تومان`;
    }

    // دریافت CSRF Token
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
});

