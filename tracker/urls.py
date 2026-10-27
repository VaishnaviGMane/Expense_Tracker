
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("register/", views.register, name="register"),
    
    path("reports/", views.reports, name="reports"),
    
    path("budgets/", views.budgets, name="budgets"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="tracker/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "transactions/",
        views.transaction_list,
        name="transaction_list",
    ),

    path(
        "transactions/add/",
        views.add_transaction,
        name="add_transaction",
    ),

    path(
        "categories/add/",
        views.add_category,
        name="add_category",
    ),

    # Reports page
    path(
        "reports/",
        views.reports,
        name="reports",
    ),
]
