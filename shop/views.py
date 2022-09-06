from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product, Contact, Order, OrderUpdate, Cart, PromoCode, TempAmount, Extra_fields, default_image
import json
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.mail import send_mail
from django.forms.models import model_to_dict
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def order_confirm(customer_email, name, id):
    subject = 'Order Confirmation'
    message = f'Hi {name}, Your order has been successfully placed. Your order id is {id}. You can track your order using this id.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [customer_email]
    send_mail(subject, message, email_from, recipient_list)

def send_contact_msg(name, email, subject, message):
    subject = subject
    message = f'Name - {name}\nEmail - {email}\n{message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ajayverma6367006928@gmail.com']
    send_mail(subject, message, email_from, recipient_list)

def all_products(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                product_obj = Product.objects.get(id=product_id)
                if product_obj:
                    cart_item = Cart(price=product_obj.price,
                                     product=product_obj)
                    cart_item.save()
                    cart_items = Cart.objects.all()
                    len_cart = len(cart_items)
                    response = {
                        'success': 'Item added to cart.',
                        'len_cart': len_cart
                    }
                    return JsonResponse(response)
                else:
                    response = {
                        'error': 'Please try again!'
                    }
                    return JsonResponse(response)
            except Exception as e:
                pass
    if request.user.is_authenticated:
        temp_amtt = TempAmount.objects.all().last()
        temp_amtt.temp_amt = 0
        temp_amtt.save()
        order = Order.objects.all().last()
        if order:
            if order.payment_status == False:
                order.delete()
        order_update = OrderUpdate.objects.all().last()
        if order_update:
            if order_update.payment_status == False:
                order_update.delete()    
        allprods = Product.objects.all()
        all_cats = {''}
        for item in allprods:
            all_cats.add(item.category)
        all_cats.remove('')
        all_cats = list(all_cats)
        cart_items = Cart.objects.values_list('product__name', flat=True)
        cart_items_list = [cart_items for cart_items in cart_items]
        len_cart = len(cart_items)
        params = {'allprods': allprods, 'all_cats': all_cats,
                  'len_cart': len_cart, 'cart_items_list': cart_items_list}
        return render(request, 'shop/all_products.html', params)
    allprods = Product.objects.all()
    all_cats = {''}
    for item in allprods:
        all_cats.add(item.category)
    all_cats.remove('')
    all_cats = list(all_cats)
    len_cart = 0
    params = {'allprods': allprods, 'all_cats': all_cats,
              'len_cart': len_cart}
    return render(request, 'shop/all_products.html', params)

def index(request):
    if request.method == 'POST':
        category = request.POST.get('cat_value')
        product_id = request.POST.get('product_id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        id = request.POST.get('id')
        forget_username = request.POST.get('forget_username')
        pass1 = request.POST.get('pass1')
        if category:
            if category == 'All Category':
                pass
            else:
                if request.user.is_authenticated:
                    allprods = Product.objects.filter(sub_category=category)
                    cart_items = Cart.objects.values_list(
                        'product__name', flat=True)
                    cart_items_list = [cart_items for cart_items in cart_items]
                    len_cart = len(cart_items_list)
                    allprods1 = Product.objects.all()
                    all_cats = {''}
                    for item in allprods1:
                        all_cats.add(item.sub_category)
                    all_cats.remove('')
                    all_cats = list(all_cats)
                    all_cats.remove(category)
                    all_cats.append('All Category')
                    params = {'allprods': allprods, 'all_cats': all_cats, 'category': category,
                              'len_cart': len_cart, 'cart_items_list': cart_items_list}
                    return render(request, 'shop/index.html', params)
                else:
                    allprods = Product.objects.filter(sub_category=category)
                    cart_items = Cart.objects.values_list(
                        'product__name', flat=True)
                    len_cart = 0
                    allprods1 = Product.objects.all()
                    all_cats = {''}
                    for item in allprods1:
                        all_cats.add(item.sub_category)
                    all_cats.remove('')
                    all_cats = list(all_cats)
                    all_cats.remove(category)
                    all_cats.append('All Category')
                    params = {'allprods': allprods, 'all_cats': all_cats, 'category': category,
                              'len_cart': len_cart}
                    return render(request, 'shop/index.html', params)
        elif product_id:
            try:
                product_obj = Product.objects.get(id=product_id)
                if product_obj:
                    cart_item = Cart(price=product_obj.price,
                                     product=product_obj)
                    cart_item.save()
                    cart_items = Cart.objects.all()
                    len_cart = len(cart_items)
                    response = {
                        'success': 'Item added to cart.',
                        'len_cart': len_cart
                    }
                    return JsonResponse(response)
                else:
                    response = {
                        'error': 'Please try again!'
                    }
                    return JsonResponse(response)
            except Exception as e:
                pass
        elif fname and lname and email:
            try:
                image = request.FILES['image']
            except Exception as e:
                dflt_image = default_image.objects.all()
                image = dflt_image[0].image
            new_user = Extra_fields.objects.get(id = id)
            new_user.first_name = fname
            new_user.last_name = lname
            new_user.email = email
            new_user.image = image
            new_user.save()
            response = {
                'success': 'Changes saved'
            }
            return JsonResponse(response)
        elif password and c_password and id:
            new_user = Extra_fields.objects.get(id = id)
            new_user.set_password(password)
            new_user.save()
            response = {
                'success': 'Changes Saved'
            }
            return JsonResponse(response)
        elif forget_username and pass1:
            try:
                user = Extra_fields.objects.get(username = forget_username)
                user.set_password(pass1)
                user.save()
                response = {
                    'success': 'Password saved successfully.'
                }
                return JsonResponse(response)
            except Exception as e:
                response = {
                    'error': 'Please try agian.'
                }
                return JsonResponse(response)
        elif forget_username:
            try:
                user = Extra_fields.objects.get(username = forget_username)
                response = {
                    'success': 'Username matched'
                }
                return JsonResponse(response)
            except Exception as e:
                response = {
                    'error': 'Username does not exists, please enter correct username.'
                }
                return JsonResponse(response)
    if request.user.is_authenticated:
        temp_amtt = TempAmount.objects.all().last()
        temp_amtt.temp_amt = 0
        temp_amtt.save()
        order = Order.objects.all().last()
        if order:
            if order.payment_status == False:
                order.delete()
        order_update = OrderUpdate.objects.all().last()
        if order_update:
            if order_update.payment_status == False:
                order_update.delete()
        allprods = Product.objects.all()
        all_cats = {''}
        for item in allprods:
            all_cats.add(item.sub_category)
        all_cats.remove('')
        all_cats = list(all_cats)
        cart_items = Cart.objects.values_list('product__name', flat=True)
        cart_items_list = [cart_items for cart_items in cart_items]
        len_cart = len(cart_items)
        params = {'allprods': allprods, 'all_cats': all_cats,
                  'len_cart': len_cart, 'cart_items_list': cart_items_list}
        return render(request, 'shop/index.html', params)
    allprods = Product.objects.all()
    all_cats = {''}
    for item in allprods:
        all_cats.add(item.sub_category)
    all_cats.remove('')
    all_cats = list(all_cats)
    len_cart = 0
    params = {'allprods': allprods, 'all_cats': all_cats,
              'len_cart': len_cart}
    return render(request, 'shop/index.html', params)


def search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        temp_prods = Product.objects.all()
        cart_items = Cart.objects.values_list('product__name', flat=True)
        cart_items_list = [cart_items for cart_items in cart_items]
        len_cart = len(cart_items)
        allprods = []
        for product in temp_prods:
            if query in product.name.lower() or query in product.description.lower() or query in product.category.lower() or query in product.name or query in product.description or query in product.category:
                allprods.append(product)
        allprods_len = len(allprods)
        if request.user.is_authenticated:
            params = {'allprods': allprods,
                    'allprods_len': allprods_len, 'query': query, 'len_cart': len_cart, 'cart_items_list': cart_items_list}
            return render(request, 'shop/search.html', params)
        else:
            len_cart = 0
            params = {'allprods': allprods,
                    'allprods_len': allprods_len, 'query': query, 'len_cart': len_cart}
            return render(request, 'shop/search.html', params)
    return render(request, 'shop/error.html')        
def about(request):
    temp_amtt = TempAmount.objects.all().last()
    temp_amtt.temp_amt = 0
    temp_amtt.save()
    order = Order.objects.all().last()
    if order:
        if order.payment_status == False:
            order.delete()
    order_update = OrderUpdate.objects.all().last()
    if order_update:
        if order_update.payment_status == False:
            order_update.delete()
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        new_contact = Contact(name=name, email=email,
                            subject=subject, message=message)
        if new_contact.save:
            send_contact_msg(name, email, subject, message)
            response = {
                'success': 'Message sent successfully!'
            }
            return JsonResponse(response)
    temp_amtt = TempAmount.objects.all().last()
    temp_amtt.temp_amt = 0
    temp_amtt.save()
    order = Order.objects.all().last()
    if order:
        if order.payment_status == False:
            order.delete()
    order_update = OrderUpdate.objects.all().last()
    if order_update:
        if order_update.payment_status == False:
            order_update.delete()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        order_Id = request.POST.get('order_Id', '')
        # email = request.POST.get('email', '')
        if order_Id == '':
            response = {
                'error': "Please enter your order id!"
            }
            return JsonResponse(response)
        else:
            try:
                order_update = OrderUpdate.objects.get(
                    order_Id=order_Id)
                if order_update.update_choice == 'Your order has been successfully placed.':
                    placed_class = 'active'
                elif order_update.update_choice == 'Your order has been picked by courier.':
                    placed_class = 'active'
                    courier_class = 'active'
                elif 'Your order reached at' in order_update.update_choice:
                    placed_class = 'active'
                    courier_class = 'active'
                    recived_class = 'active'
                else:
                    placed_class = 'active'
                    courier_class = 'active'
                    recived_class = 'active'
                    dilivered = 'active'

                html = render_to_string(
                    'shop/dynamic_tracker.html',
                    locals()
                )
                return HttpResponse(json.dumps(
                    {'html': html, 'status': True}), content_type="application/json")
            except Exception as e:
                response = {
                    'error': "Please enter corret order id!"
                }
                return JsonResponse(response)
    temp_amtt = TempAmount.objects.all().last()
    temp_amtt.temp_amt = 0
    temp_amtt.save()
    order = Order.objects.all().last()
    if order:
        if order.payment_status == False:
            order.delete()
    order_update = OrderUpdate.objects.all().last()
    if order_update:
        if order_update.payment_status == False:
            order_update.delete()
    return render(request, 'shop/tracker.html')


def my_orders(request):
    temp_amtt = TempAmount.objects.all().last()
    temp_amtt.temp_amt = 0
    temp_amtt.save()
    order = Order.objects.all().last()
    if order:
        if order.payment_status == False:
            order.delete()
    order_update = OrderUpdate.objects.all().last()
    if order_update:
        if order_update.payment_status == False:
            order_update.delete()
    orders = Order.objects.all()
    return render(request, 'shop/my_orders.html', {'orders': orders})


def productview(request, id):
    temp_amtt = TempAmount.objects.all().last()
    temp_amtt.temp_amt = 0
    temp_amtt.save()
    order = Order.objects.all().last()
    if order:
        if order.payment_status == False:
            order.delete()
    order_update = OrderUpdate.objects.all().last()
    if order_update:
        if order_update.payment_status == False:
            order_update.delete()
    prod = Product.objects.filter(id=id)
    prods = Product.objects.all()
    desc = prod[0].description
    cart_items = Cart.objects.values_list('product__name', flat=True)
    cart_items_list = [cart_items for cart_items in cart_items]
    len_cart = len(cart_items)
    if ". " in desc:
            for index, char in enumerate(desc):
                if (desc[index] == "." and desc[index + 1] == " "):
                    desc = desc.split(". ")
                    break
    else:
        desc = [desc]
    if request.user.is_authenticated:  
        return render(request, 'shop/productview.html', {'product': prod[0], 'desc': desc, 'prods': prods, 'len_cart': len_cart, 'cart_items_list': cart_items_list})
    else:
        len_cart = 0
        return render(request, 'shop/productview.html', {'product': prod[0], 'desc': desc, 'prods': prods, 'len_cart': len_cart})


def cart(request):
    if request.method == 'POST':
        qty = request.POST.get('qty')
        id = request.POST.get('id')
        prod_id = request.POST.get('prod_id')
        promo_code = request.POST.get('promo_code')
        if qty:
            qty = int(qty)
            amount = 0
            shipping_amount = float(40)
            if qty > 0:
                cart_item = Cart.objects.get(product__id=id)
                cart_item.qty = qty
                cart_item.price = cart_item.product.price * cart_item.qty
                cart_item.save()
                cart_items = Cart.objects.all()
                for item in cart_items:
                    amount = amount + item.price
                total_amount = amount + shipping_amount
                response = {
                    'success': 'Cart Updated',
                    'amount': amount,
                    'total_amount': total_amount
                }
                return JsonResponse(response)
            else:
                cart_item = Cart.objects.get(product__id=id)
                cart_item.delete()
                cart_items = Cart.objects.all()
                amount = 0
                shipping_amount = float(40)
                for item in cart_items:
                    amount = amount + item.price
                total_amount = amount + shipping_amount
                cart_len = len(Cart.objects.all())
                if cart_len == 0:
                    response = {
                        'success1' : 'Cart Updated',
                        'reload' : 'Yes'
                    }
                    return JsonResponse(response)
                else:
                    response = {
                        'success' : 'Cart Updated',
                        'amount': amount,
                        'total_amount': total_amount
                    }
                    return JsonResponse(response)
        elif prod_id:
            try:
                cart_item = Cart.objects.get(product__id = prod_id)
                cart_item.delete()
                cart_items = Cart.objects.all()
                amount = 0
                shipping_amount = float(40)
                for item in cart_items:
                    amount = amount + item.price
                total_amount = amount + shipping_amount
                cart_len = Cart.objects.all()
                cart_len = len(cart_len)
                if cart_len == 0:
                    response = {
                        'success1' : 'Item Removed',
                        'reload' : 'Yes'
                    }
                    return JsonResponse(response)
                else:
                    response = {
                        'success' : 'Item Removed',
                        'amount': amount,
                        'total_amount': total_amount
                    }
                    return JsonResponse(response)
            except Exception as e:
                pass
        elif promo_code:
            p_code = PromoCode.objects.all()
            for code in p_code:
                if code.promo_code == promo_code:
                    cart_items = Cart.objects.all()
                    temp_amtt = TempAmount.objects.all().first()
                    amount = 0
                    shipping_amount = float(40)
                    for item in cart_items:
                        amount = amount + item.price
                    total_amount = amount + shipping_amount
                    print(total_amount, code.promo_amount, 'llllllllllllllllllllll')
                    if total_amount > code.promo_amount:
                        total_amount = total_amount - code.promo_amount
                        temp_amtt.temp_amt = total_amount
                        temp_amtt.save()
                        response = {
                            'success': "Code Applied",
                            'promo_amount': code.promo_amount,
                            'total_amount': total_amount
                        }    
                        return JsonResponse(response)
                    else:
                        response = {
                            'error': "Please enter correct promo code!"
                        }
                        return JsonResponse(response)
            else:
                response = {
                    'error': "Please enter correct promo code!"
                }
                return JsonResponse(response)
        else:
            cart_items = Cart.objects.all()
            if len(cart_items) > 0:
                Cart.objects.all().delete()
                response = {
                    'success': 'Cart cleared.'
                }
                return JsonResponse(response)
            else:
                response = {
                    'error': 'Cart already cleared.!'
                }
                return JsonResponse(response)
    if request.user.is_authenticated:
        temp_amtt = TempAmount.objects.all().last()
        temp_amtt.temp_amt = 0
        temp_amtt.save()
        order = Order.objects.all().last()
        if order:
            if order.payment_status == False:
                order.delete()
        order_update = OrderUpdate.objects.all().last()
        if order_update:
            if order_update.payment_status == False:
                order_update.delete()   
        cart_items = Cart.objects.all()
        len_cart = len(cart_items)
        amount = 0
        shipping_amount = float(40)
        if len_cart == 0:
            return render(request, 'shop/error.html')
        else:
            for item in cart_items:
                amount = amount + item.price
            total_amount = amount + shipping_amount
            params = {'cart_items': cart_items, 'amount': amount, 'shipping_amount': shipping_amount, 'total_amount': total_amount}
            return render(request, 'shop/cart.html', params)            
    return render(request, 'shop/error.html')


def checkout(request):
    if request.user.is_authenticated:
        temp_amtt = TempAmount.objects.all().first()
        if temp_amtt.temp_amt > 0:
            total_amount = temp_amtt.temp_amt
            if request.method == "POST":
                total_amount = total_amount
                currency = 'INR'
                amount = total_amount * 100  # Rs. 200
                # Create a Razorpay Order
                razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                                currency=currency,
                                                                payment_capture='0'))

                # order id of newly created order.
                razorpay_order_id = razorpay_order['id']
                callback_url = '/payment_handler'

                # we need to pass these details to frontend.
                context = {}
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                context['razorpay_amount'] = amount
                context['currency'] = currency
                context['callback_url'] = callback_url
                return JsonResponse(context)
            return render(request, 'shop/checkout.html', {'total_amount': total_amount})
            # return render(request, 'shop/checkout.html', {"cart_items": cart_items, 'total_amount': total_amount, 'total_qty': total_qty})
        else:    
            cart_items = Cart.objects.all()
            total_amount = 0
            shipping_amount = float(40)
            # total_qty = 0
            for item in cart_items:
                total_amount = total_amount + item.price
                # total_qty = total_qty + int(item.qty)
            total_amount = total_amount + shipping_amount
            temp_amtt = TempAmount.objects.all().first()
            if temp_amtt.temp_amt > 0:
                total_amount = temp_amtt.temp_amt
            if request.method == "POST":
                total_amount = total_amount
                currency = 'INR'
                amount = total_amount * 100  # Rs. 200
                # Create a Razorpay Order
                razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                                currency=currency,
                                                                payment_capture='0'))

                # order id of newly created order.
                razorpay_order_id = razorpay_order['id']
                callback_url = '/payment_handler'

                # we need to pass these details to frontend.
                context = {}
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                context['razorpay_amount'] = amount
                context['currency'] = currency
                context['callback_url'] = callback_url
                return JsonResponse(context)
            return render(request, 'shop/checkout.html', {'total_amount': total_amount})
            # return render(request, 'shop/checkout.html', {"cart_items": cart_items, 'total_amount': total_amount, 'total_qty': total_qty})
    return render(request, 'shop/error.html')


def checkout_done(request):
    if request.method == "POST":
        # allitems = request.POST.get('allitems')
        # amount = request.POST.get('amount')
        cart_items = Cart.objects.all()
        amount = 0
        shipping_amount = float(40)
        for item in cart_items:
            amount = amount + item.price
        amount = amount + shipping_amount
        temp_amtt = TempAmount.objects.all().first()
        if temp_amtt.temp_amt > 0:
            amount = temp_amtt.temp_amt
        name = request.POST.get('name')
        email = request.POST.get('email')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        session_list = []
        session_list.append(amount)
        if (len(name) > 2 or len(city) > 2 or len(state) > 2 or len(phone) > 9):
            pass
            order = Order(amount=amount, payment_status= False, name=name, email=email, address_line1=address_line1,
                          address_line2=address_line2, city=city, state=state, phone=phone, zip_code=zip_code)
            order.save()
            order_update = OrderUpdate(
                order_Id=order.id, payment_status= False)
            order_update.save()
            Id = order.id
            session_list.append(Id)
            session_list.append(email)
            session_list.append(name)
            request.session['session_data'] = session_list
            response = {
                'msg': f'Your order has been successfully placed, your order id is {Id}, user this id to track your order!'
            }
            return JsonResponse(response)
    return render(request, 'shop/error.html')


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def payment_handler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is True:
                amount = request.session['session_data'][0]*100
                # amount = 1439.0
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    customer_email = request.session['session_data'][2]
                    id = request.session['session_data'][1]
                    name = request.session['session_data'][3]
                    order_confirm(customer_email, name, id)
                    order = Order.objects.all().last()
                    order.payment_status = True
                    order.save()
                    order_update = OrderUpdate.objects.all().last()
                    order_update.payment_status = True
                    order_update.save()
                    temp_amtt = TempAmount.objects.all().last()
                    temp_amtt.temp_amt = 0
                    temp_amtt.save()
                    cart = Cart.objects.all().delete()
                    # render success page on successful caputre of payment
                    # return HttpResponse('success page on successful caputre of payment')
                    return render(request, 'shop/payment_handler.html', {'message': 'Your order has been successfully placed.'})
                except Exception as e:
                    try:
                        order_id = request.session['session_data'][1]
                        order = Order.objects.get(id=order_id)
                        order.delete()
                        # if there is an error while capturing payment.
                        # return HttpResponse('there is an error while capturing payment')
                        return render(request, 'shop/payment_handler.html', {'message': 'Your payment was not capturing, please try again.'})
                    except Exception as e:
                        pass
                    return HttpResponse("404 - Not Found")
            else:
                try:
                    order = Order.objects.get(
                        order_id=request.session['current_order_id'])
                    order.delete()
                    # if signature verification fails.
                    # return HttpResponse('signature verification fails.')
                    return render(request, 'shop/payment_handler.html', {'message': 'Signature verification failed, please try again.'})
                except Exception as e:
                    pass
                return HttpResponse("404 - Not Found")
        except:
            # if we don't find the required parameters in POST data
            return render(request, 'shop/error.html')
    else:
        # if other than POST request is made.
        return render(request, 'shop/error.html')
    return render(request, 'shop/error.html')    


def sign_up(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if fname and lname and email and username and password and c_password:
            # try:
            #     user = User.objects.get(username = username)
            # if user:
            #     response = {
            #         'error': 'Entered username already exists. Please try different username!'
            #     }
            #     return JsonResponse(response)
            # else:
            if password == c_password:
                new_user = Extra_fields.objects.create_user(username, email, password)
                new_user.first_name = fname
                new_user.last_name = lname
                new_user.image = default_image.objects.all().first().image
                new_user.save()
                response = {
                    'success': 'Your account successfully created!'
                }
                return JsonResponse(response)
            else:
                response = {
                    'error': 'Password not matched!'
                }
                return JsonResponse(response)
            # except Exception as e:
            #     pass
        else:
            response = {
                'error': 'Please fill these all details!'
            }
            return JsonResponse(response)
    return render(request, 'shop/error.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                response = {
                    'success': 'Sign in successfully!'
                }
                return JsonResponse(response)
            else:
                response = {
                    'error': 'Please enter correct username or password!'
                }
            return JsonResponse(response)
        else:
            response = {
                'error': 'Please enter username and password!'
            }
            return JsonResponse(response)
    return render(request, 'shop/error.html')


def logOut(request):
    if request.method == 'POST':
        logout(request)
        response = {
            'success': 'Logout Successfully!!'
        }
        return JsonResponse(response)
    return render(request, 'shop/error.html')
