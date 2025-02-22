from api.utils import get_price, get_subtotal, apply_promo
from api.models import Product

from .settings import DEFAULT_PRICE


def test_get_price():
    product_ids = []
    for index in range(2):
        id = index + 1
        product = Product(id=id)
        product_ids.append(product.id)
    prices = {id: id * DEFAULT_PRICE for id in product_ids}
    assert prices == get_price(product_ids)


def test_get_subtotal():
    product_id_1 = 1
    product_id_2 = 2
    qty_1 = 3
    qty_2 = 2
    cart = {
        'cart_items': [
            {
                'product_id': product_id_1,
                'qty': qty_1
            },
            {
                'product_id': product_id_2,
                'qty': qty_2
            },
        ]
    }
    assert sum([DEFAULT_PRICE * product_id_1 * qty_1, DEFAULT_PRICE * product_id_2 * qty_2]) == get_subtotal(cart)['subtotal']


def test_apply_promo():
    subtotal = 200000.0
    shipping_fee = 15000.0

    promotion = {
        'coupon_code': 'XYZ',
        'subtotal_discount': 10, # percentage
        'max_subtotal_discount': 13500, # rate
        'shipping_discount': 100,  # percentage
        'max_shipping_discount': 20000, # rate
        'cashback': 5,
        'max_cashback': 50000
    }

    subtotal_discount = 13500
    shipping_discount = 15000
    cashback = 10000

    applied_promo = apply_promo(subtotal, shipping_fee, promotion)

    # subtotal discount
    assert subtotal_discount == applied_promo['subtotal_discount']
    # shipping fee
    assert shipping_discount == applied_promo['shipping_discount']
    # cashback
    assert cashback == applied_promo['cashback']

