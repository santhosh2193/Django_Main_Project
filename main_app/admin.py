from django.contrib import admin
from .models import Book, Member, Transaction

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("Title", "Author", "Category", "Available")
    list_filter = ("Available", "Category")
    search_fields = ("Title", "Author")

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "membership_date")
    search_fields = ("user__username",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("book", "member", "issue_date", "return_date", "fine")
    list_filter = ("issue_date", "return_date")
    search_fields = ("book__Title", "member__user__username")


# Register your models here.
