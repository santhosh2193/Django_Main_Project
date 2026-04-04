from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm,CustomUserCreationForm
import datetime
from .models import Transaction,User,Book,Member
from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your views here.

def home(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)   # logs the user in
            return redirect("dashboard")  # redirect to homepage after login
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ✅ Avoid duplicate member creation
            Member.objects.get_or_create(user=user)
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


@login_required
def borrow_book(request, book_id):
    # Get the book object
    book = get_object_or_404(Book, id=book_id)

    # Check if book is available
    if not book.Available:
        messages.error(request, "Sorry, this book is not available.")
        return redirect("dashboard")

    # Get the logged-in user's Member profile
    member = get_object_or_404(Member, user=request.user)

    # Create a new transaction
    Transaction.objects.create(
        book=book,
        member=member,
        issue_date=datetime.date.today()
    )

    # Mark book as unavailable
    book.Available = False
    book.save()

    messages.success(request, f"You have borrowed '{book.Title}'.")
    return redirect("dashboard")



@login_required
def return_book(request, transaction_id):
    # Get the transaction object
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Ensure the book hasn't already been returned
    if transaction.return_date:
        messages.warning(request, "This book has already been returned.")
        return redirect("dashboard")

    # Set return date
    transaction.return_date = datetime.date.today()

    # Optional fine calculation (example: Rs.10 per day after 14 days)
    issue_period = (transaction.return_date - transaction.issue_date).days
    allowed_days = 14
    fine_per_day = 10

    if issue_period > allowed_days:
        transaction.fine = (issue_period - allowed_days) * fine_per_day

    transaction.save()

    # Mark book as available again
    book = transaction.book
    book.Available = True
    book.save()

    messages.success(request, f"You have returned '{book.Title}'. Fine: ₹{transaction.fine}")
    return redirect("dashboard")



@login_required
def dashboard(request):
    member, created = Member.objects.get_or_create(user=request.user)
    available_books = Book.objects.filter(Available=True)
    borrowed_books = Transaction.objects.filter(member=member, return_date__isnull=True)
    transactions = Transaction.objects.filter(member=member)

    return render(request, "dashboard.html", {
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "transactions": transactions,
    })


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@staff_required
def add_book(request):
    # Only staff can access this view
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        Book.objects.create(Title=title, Author=author, Category=category, Available=True)
        messages.success(request, f"Book '{title}' added successfully.")
        return redirect("dashboard")
    return render(request, "add_book.html")


@receiver(post_save, sender=User)
def create_member_for_new_user(sender, instance, created, **kwargs):
    if created:
        Member.objects.get_or_create(user=instance)



@login_required
def logout_view(request):
    logout(request)  # clears the session
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")  # redirect to login page