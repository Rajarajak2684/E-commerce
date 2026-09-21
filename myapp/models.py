from django.db import models

# Create your models here.
class products(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    qty=models.IntegerField(default=1)
    desc=models.TextField()
    product_image=models.ImageField(upload_to='product_images/',null=True,blank=True)
    created_by=models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='created_products')
    created_at=models.DateTimeField(auto_now_add=True)
    
class UserCart(models.Model):
    user=models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name='user_cart')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def _init_(self):
        return self.user.username
    
class CartItems(models.Model):
    cart=models.ForeignKey(UserCart,on_delete=models.CASCADE,related_name='cart_items')
    product=models.ForeignKey(products,on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"""{self.quantity}of {self.product.name}in
        {self.cart.user.username}'s cart"""
    