from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'shophome'),
    path('all_products', views.all_products, name = 'all_products'),
    path('about', views.about, name = 'about'),
    path('contact', views.contact, name = 'contact'),
    path('tracker', views.tracker, name = 'tracker'),
    path('search', views.search, name = 'search'),
    path('my_orders', views.my_orders, name = 'my_orders'),
    path('productview/<int:id>/<str:name>', views.productview, name = 'product_view'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('checkout_done', views.checkout_done, name = 'checkout_done'),
    # path('make_payment', views.make_payment, name = 'make_payment'),
    path('payment_handler', views.payment_handler, name = 'payment_handler'),
    path('sign_up', views.sign_up, name = 'sign_up'),
    path('sign_in', views.sign_in, name = 'sign_in'),
    path('logout', views.logOut, name = 'logout'),
    path('profile', views.profile, name = 'profile'),
    path('account', views.account, name = 'account'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)