
from django import forms
from .models import Transaction, Category, Budget


class TransactionForm(forms.ModelForm):

    transaction_type = forms.ChoiceField(
        choices=Transaction.TYPE_CHOICES,
        label="Transaction Type",
        widget=forms.Select(
            attrs={"class": "form-select"}
        )
    )

    class Meta:
        model = Transaction
        fields = [
            "category",
            "transaction_type",
            "amount",
            "description",
            "date",
        ]

        widgets = {
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (
            Category.objects.filter(user=self.user)
        )

        self.fields["category"].empty_label = (
            "Select a category"
        )

        self.fields["transaction_type"].choices = [
            ("", "Select transaction type"),
            *Transaction.TYPE_CHOICES,
        ]


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter category name",
                }
            ),
        }


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = [
            "category",
            "month",
            "limit_amount",
        ]

        widgets = {
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),
            "month": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "limit_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter budget limit",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (
            Category.objects.filter(user=self.user)
        )

        self.fields["category"].empty_label = (
            "Select a category"
        )
