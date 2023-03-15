function googleTranslateElementInit() {
    new google.translate.TranslateElement({ pageLanguage: 'en' }, 'google_translate_element');
    $('.goog-logo-link').remove()
    $('.skiptranslate').css("margin-bottom", "-17px")
    $('.lang_box').css({ "margin-top": "3px", "margin-left": "25px" })
    $('*:contains("Powered by")').each(function () {
       if ($(this).children().length < 1)
          $(this).css({ "color": "#2b2a29" })
    });
}
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

$('.no_cart').on('click', function () {
    toastr.info('Please sign in to your account for use cart!')
    $('.toast').css('background-color', '#2f96b4');
 })
 $('.check_cat').on('click', function () {
    $(this).attr('name', 'crnt_cat_value');
    $('.check_cat').val('');
    let cate_name = $(this).next().text().trim().replace('\n', '');
    $(this).val(cate_name);
    $('#cat_form_id').submit();
 })

 $('#cart_btn').on('click', function () {
    if ($('#cart_len').text() > 0) {
       window.location = '/cart';
    }
    else {
       toastr.info('Your cart is empty, Please add some items in your cart!');
       $('.toast').css('background-color', '#2f96b4');
    }
 });

 $('.cart').on('click', function () {
    let self = $(this);
    let product_id = self.attr('data-id');
    data = {
       'product_id': product_id,
       'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
       type: 'POST',
       url: "{% url 'shophome' %}",
       data: data,
       success: function (data) {
          if (data.success == 'Item added to cart.') {
             $('#cart_len').text(data.len_cart);
             toastr.success(data.success);
             $('.toast').css('background-color', '#51a351');
             self.removeClass('cart');
             self.text('Added to Cart');
             self.addClass("disabled")
          }
          else {
             toastr.success(data.error);
             $('.toast').css('background-color', '#bd362f');
          }
       }
    })
 })