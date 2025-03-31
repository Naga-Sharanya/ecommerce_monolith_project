from django.db import models

# Create your models here.
from django.db import models
from usermanagement.models import User
from products_app.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)


class CartItemExtra(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="extras")
    option_name = models.CharField(max_length=100)
    option_value = models.CharField(max_length=100)

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        max_length=10, choices=[("fixed", "Fixed"), ("percentage", "Percentage")]
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField()


class AppliedCoupon(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
