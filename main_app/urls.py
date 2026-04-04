from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("",views.home),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("dashboard/",views.dashboard, name = "dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("borrow/<int:book_id>/", views.borrow_book, name="borrow_book"),
    path("return/<int:transaction_id>/", views.return_book, name="return_book"),
    path("add-book/", views.add_book, name="add_book"),
    path("logout/", views.logout_view, name="logout"),

]
