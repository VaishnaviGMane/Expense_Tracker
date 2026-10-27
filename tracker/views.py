
from datetime import date

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Transaction, Category, Budget
from .forms import TransactionForm, CategoryForm, BudgetForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "tracker/register.html", {
        "form": form
    })


@login_required
def dashboard(request):
    today = date.today()
    transactions = Transaction.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month,
    )

    income = transactions.filter(
        transaction_type="income"
    ).aggregate(total=Sum("amount"))["total"] or 0

    expenses = transactions.filter(
        transaction_type="expense"
    ).aggregate(total=Sum("amount"))["total"] or 0

    recent_transactions = transactions.order_by("-date", "-id")[:5]

    return render(request, "tracker/dashboard.html", {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
        "recent_transactions": recent_transactions,
    })


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related("category").order_by("-date", "-id")

    return render(request, "tracker/transaction_list.html", {
        "transactions": transactions
    })


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(user=request.user)

    return render(request, "tracker/transaction_form.html", {
        "form": form
    })


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("add_transaction")
    else:
        form = CategoryForm()

    return render(request, "tracker/category_form.html", {
        "form": form
    })


@login_required
def reports(request):
    today = date.today()

    transactions = Transaction.objects.filter(
        user=request.user,
        transaction_type="expense",
        date__year=today.year,
    )

    category_data = (
        transactions.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("category__name")
    )

    labels = [
        row["category__name"]
        for row in category_data
    ]

    values = [
        float(row["total"])
        for row in category_data
    ]

    monthly_labels = []
    monthly_income = []
    monthly_expenses = []

    for month in range(1, 13):
        monthly = Transaction.objects.filter(
            user=request.user,
            date__year=today.year,
            date__month=month,
        )

        inc = monthly.filter(
            transaction_type="income"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        exp = monthly.filter(
            transaction_type="expense"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        monthly_labels.append(
            date(today.year, month, 1).strftime("%b")
        )
        monthly_income.append(float(inc))
        monthly_expenses.append(float(exp))

    return render(
        request,
        "tracker/reports.html",
        {
            "category_labels": labels,
            "category_values": values,
            "monthly_labels": monthly_labels,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "report_year": today.year,
        },
    )



@login_required
def budgets(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, user=request.user)

        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.month = budget.month.replace(day=1)
            budget.save()
            return redirect("budgets")
    else:
        form = BudgetForm(user=request.user)

    current_month = timezone.localdate().replace(day=1)

    budget_items = Budget.objects.filter(
        user=request.user,
        month=current_month,
    ).select_related("category")

    for budget in budget_items:
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            transaction_type="expense",
            date__year=current_month.year,
            date__month=current_month.month,
        ).aggregate(total=Sum("amount"))["total"] or 0

        budget.spent = spent
        budget.remaining = budget.limit_amount - spent

    return render(request, "tracker/budgets.html", {
        "form": form,
        "budget_items": budget_items,
    })
