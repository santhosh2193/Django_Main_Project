from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Category = models.CharField(max_length=255)
    Available = models.BooleanField(default=True)

    def __str__(self):
        return self.Title

class Member(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
         return self.user.username
    
class Transaction(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True,blank=True)
    fine = models.DecimalField(max_digits=6 , decimal_places=2 ,default=0)

    def __str__(self):
        return f"Transaction: {self.book.Title} by {self.member.user.username}"


