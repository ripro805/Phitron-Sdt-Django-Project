from django.db import models
from users.models import User
from product.models import Product

class Cart(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Cart of {self.user.email}"

class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()

	def __str__(self):
		return f"{self.quantity} x {self.product.name} in {self.cart.user.email}'s cart"


# Order and OrderItem models
class Order(models.Model):
	STATUS_CHOICES = [
		('PENDING', 'Pending'),
		('SHIPPED', 'Shipped'),
		('DELIVERED', 'Delivered'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Order #{self.id} by {self.user.email}"

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
