from django.shortcuts import render
from django import views
from .forms import CreateBudgetForm, TransactionForm
from .models import Budget, Category, Transaction
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import json

@login_required
def userprofile_view(request):
    return render(request, 'base-user.html')
    

def dashboard(request):
    if request.method == 'POST':
        form = CreateBudgetForm(request.POST, request=request)
        if form.is_valid():
            cd = form.cleaned_data
            category = Category.objects.create(name=cd['category'], user=request.user)
            budget = Budget(
                user=request.user,
                amount=cd['amount'],
                current_amount=cd['amount'],
                category=category ,
                start_date=cd['start_date'],
                end_date=cd['end_date']
                )
            budget.save()
            new_balance = Budget.objects.aggregate(total=Sum('current_amount'))['total'] or 0
            return JsonResponse({'status': 'success', 'new_balance': new_balance, 'amount': cd['amount'], 'category' : cd['category']})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    elif request.method == 'GET':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            balance = Budget.objects.aggregate(total=Sum('amount'))['total'] or 0
            transaction_expense = Transaction.objects.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
            balance = balance - transaction_expense
            transaction_income = Transaction.objects.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
            balance = balance + transaction_income
            categories = Category.objects.all()
            total_income = Transaction.total_income()
            total_expense = Transaction.total_expense()
            budget_names = Budget.objects.all().values_list('category__name', flat=True)
            budget_amounts = Budget.objects.all().values_list('amount', flat=True)
            budget_amounts = [int(amount) for amount in budget_amounts]
            data = {
                'balance': balance,
                'categories': list(categories.values('id', 'name')),
                'total_income': total_income,
                'total_expense': total_expense,
                'labels': list(budget_names),
                'datasets': [{
                    'label': '# of Votes',
                    'data': list(budget_amounts),
                    'borderWidth': 1
                }]
            }
            return JsonResponse(data)
        else:
            return render(request, 'userprofile/dashboard.html')
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                category_budget = Budget.objects.get(user=request.user, category=cd['category'])
                if cd['transaction_type'] == 'income':
                    category_budget.current_amount += cd['amount']
                else:
                    category_budget.current_amount -= cd['amount']
                category_budget.save()
                new_transaction = form.save(commit=False)
                new_transaction.user = request.user
                new_transaction.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Transaction saved!',
                    'transaction': {
                        'id' : new_transaction.id,
                        'name' : cd['name'],
                        'amount': cd['amount'],
                        'category': cd['category'].name,
                        'transaction_type': cd['transaction_type'],
                        'date' : new_transaction.date
                    },
                    
                })
            except Budget.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Category budget does not exist.'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    elif request.method == 'GET':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            categories = Category.objects.all().values('pk', 'name')
            transactions = Transaction.objects.filter(user=request.user).order_by('-date')
            transactions_data = list(transactions.values('id','name', 'category__name', 'amount', 'transaction_type', 'date'))
            return JsonResponse({'transactions': transactions_data,
                                 'categories' : list(categories)
                                 })
        else:
            return render(request, 'userprofile/transaction.html')
    return JsonResponse({'status' : 'error', 'message' : 'Invadid'})

def delete_transaction(request, id):
    print('this function')
    if request.method == 'DELETE':
        try:
            print('try block ')
            transaction = Transaction.objects.get(pk=id)
            print(f'I find transaciton{transaction}')
            budget = Budget.objects.get(category=transaction.category, user=request.user)
            print(f'I find {budget}')
            if transaction.transaction_type == 'expense':
                print('this is if block')
                print(transaction.transaction_type)
                budget.current_amount += transaction.amount
            else:
                print('this is else block')
                print(transaction.transaction_type)
                budget.current_amount -= transaction.amount
            print('save that current amount!')
            budget.save()
            transaction.delete()
            return JsonResponse({
                'success' : True,
                'transaction_id' : id 
                                 })
        except Transaction.DoesNotExist:
            return JsonResponse({'error' : 'Transaction not found!'}, status=404)
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget not found for this transaction!'}, status=404)
    return JsonResponse({'error': 'Method not allowed!'}, status=405)


def update_transaction(request, id):
    transaction = Transaction.objects.get(pk=id)
    transaction_type = transaction.transaction_type
    transaction_category = transaction.category
    if request.method == 'GET':
        return JsonResponse({
            'transaction' : {
                'id' : transaction.id,
                'name' : transaction.name,
                'amount' : transaction.amount,
                'transaction_type' : transaction.transaction_type,
                'category' : {
                    'id' : transaction.category.id,
                    'name' : transaction.category.name
                }
            }
        })
    elif request.method == 'PUT':
        data = json.loads(request.body)
        form = TransactionForm(data, instance=transaction)
        if form.is_valid():
            update_transaction = form.save(commit=False)
            budget = Budget.objects.get(user=request.user ,category=transaction_category)
            if update_transaction.transaction_type != transaction_type:
                if update_transaction.transaction_type == 'expense':
                    transactions = Transaction.objects.filter(user=request.user, category=transaction_category, transaction_type='expense')
                    amount_expense = transactions.aggregate(total=Sum('amount'))['total'] or 0
                    double = transaction.amount * 2
                    budget.current_amount -= double
                    print(f'all amount of expence is {amount_expense}\n and my transaction is {transaction.amount}\n so we double it:{transaction.amount * 2} and - form the budget current {budget.current_amount} and my budget current will be {budget.current_amount - (transaction.amount * 2)}')

                else:
                    transactions = Transaction.objects.filter(user=request.user, category=transaction_category, transaction_type='income')
                    amount_income = transactions.aggregate(total=Sum('amount'))['total'] or 0
                    double = transaction.amount * 2
                    budget.current_amount += double
                    print(f'befor is {transaction_type}, after {update_transaction.transaction_type}')
                    print(f'All incomes are:{amount_income}\nThis transaction amount is: {transaction.amount}\n double it: {transaction.amount * 2}\n all transactions amount income + this transaction amount {amount_income + transaction.amount} the budget current should be: {budget.current_amount - (amount_income + transaction.amount)}')

            budget.save()
            update_transaction.user = request.user
            update_transaction.save()
            return JsonResponse({
                'status' : 'success',
                'message' : 'Transition updated successfully!',
                'transaction' : {
                    'id' : update_transaction.id,
                    'name' : update_transaction.name,
                    'amount' : update_transaction.amount,
                    'transaction_type' : update_transaction.transaction_type,
                    'date' : update_transaction.date,
                    'category' : {
                        'id' : update_transaction.category.id,
                        'name' : update_transaction.category.name
                    }
                }
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)


def category(request):
    budgets = Budget.objects.all()
    budgets_list = []
    for budget in budgets:
        budgets_list.append((budget, round(budget.current_amount * 100 / budget.amount)))
    return render(request, 'userprofile/category.html', {'budgets' : budgets_list})
