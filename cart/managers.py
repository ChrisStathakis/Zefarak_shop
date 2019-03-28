from django.db import models


class CartManager(models.Manager):

    def active_carts(self):
        return super(CartManager, self).filter(active=True)

    def current_cart(self, session_id):
        get_cart = super(CartManager, self).filter(id_session=session_id, active=True)
        return get_cart.last() if get_cart else None