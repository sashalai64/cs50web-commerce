from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listings") #access all listings created by a specific user using "user.listings.all()"
    item = models.CharField(max_length = 100)
    description = models.TextField()
    startingBid = models.DecimalField(max_digits = 10, decimal_places = 2)
    currentBid = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    time = models.DateTimeField(auto_now = True)
    image = models.ImageField(null = True, blank = True)
    active = models.BooleanField(default = True)
    winner = models.CharField(max_length = 100, null = True, blank = True)
    category = models.CharField(max_length = 50, choices = [
        ('Art', 'Art'),
        ('Clothing & Accessories', 'Clothing & Accessories'),
        ('Electronics', 'Electronics'),
        ('Home Goods', 'Home Goods'),
        ('Sports & Outdoor', 'Sports & Outdoor'),
        ('Books & Media', 'Books & Media'),
        ('Others', 'Others')], 
        default='Others')

    def __str__(self):
        return f'{self.user}: listed an item "{self.item}" for ${self.startingBid}'
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'bids') #access all bids placed by a specific user using "user.bids.all()"
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = 'bids') #access all bids placed on a specific listing using "listing.bids.all()"
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user}: placed a bid on "{self.item}" for ${self.price}'


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "watchlist_items") #access all items in a user's watchlist using "user.watchlist_items.all()"
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "watched_by") #access all users who have a specific listing in their watchlist using "listing.watched_by.all()"

    def __str__(self):
        return f'{self.user}: listed "{self.item}" to watchlist'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments") #access all comments made by a user using "user.comments.all()"
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments") #access all comments on a specific listing using "listing.comments.all()"
    comment = models.TextField(blank = True)
    time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user}: commented on "{self.item}": {self.comment}'