$(document).ready(function () {
    $(".add-to-cart").click(function (e) {
        e.preventDefault();

        let productId = $(this).data("product-id");
        let productItem = $(this).closest(".product-item");
        let productName = productItem.find(".name-product-item").text().trim();
        let productPrice = parseFloat(productItem.find(".main-price").text().trim());
        let productDiscount = parseFloat(productItem.find(".discount-price").text().trim()) || 0;

        $.ajax({
            type: "POST",
            url: "/add-to-cart/",
            data: {
                product_id: productId,
                product_name: productName,
                product_price: productPrice,
                product_discount: productDiscount,
                csrfmiddlewaretoken: "{{ csrf_token }}"
            },
            success: function (response) {
                if (response.success) {
                    // آپدیت تعداد محصولات و قیمت کلی
                    $("#cart-total-items").text(response.total_items);
                    $("#cart-total-price").text(response.total_price + " تومان");

                    // نمایش لینک مشاهده سبد خرید
                    productItem.find(".view-cart").show();
                }
            }
        });
    });
});
