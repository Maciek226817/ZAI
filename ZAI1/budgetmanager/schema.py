from datetime import datetime

import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Transaction, Attachment, Budget, RecurringTransaction, Goal
from django.contrib.auth.models import User
from decimal import Decimal


# Typ dla użytkownika
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Możesz dodać inne pola, które chcesz zwrócić


# Typ dla kategorii
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

    user = graphene.Field(UserType)  # Dodajemy pole user

    def resolve_user(self, info):
        return self.user  # Zwracamy powiązanego użytkownika dla kategorii

# class CategoryType(DjangoObjectType):
#     class Meta:
#         model = Category
#         fields = "__all__"


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = "__all__"


class AttachmentType(DjangoObjectType):
    class Meta:
        model = Attachment
        fields = "__all__"


class BudgetType(DjangoObjectType):
    class Meta:
        model = Budget
        fields = "__all__"
    total_expenses = graphene.Float()

    def resolve_total_expenses(self, info):
        return self.total_expenses()  # Wywołanie funkcji agregującej z modelu

class RecurringTransactionType(DjangoObjectType):
    class Meta:
        model = RecurringTransaction
        fields = "__all__"


class GoalType(DjangoObjectType):
    class Meta:
        model = Goal
        fields = "__all__"

class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_transactions = graphene.List(TransactionType)
    all_attachments = graphene.List(AttachmentType)
    all_budgets = graphene.List(BudgetType)
    all_recurring_transactions = graphene.List(RecurringTransactionType)
    all_goals = graphene.List(GoalType)

    # Pobieranie wszystkich kategorii
    def resolve_all_categories(self, info):
        return Category.objects.all()

    # Pobieranie wszystkich transakcji
    def resolve_all_transactions(self, info):
        return Transaction.objects.all()

    # Pobieranie wszystkich załączników
    def resolve_all_attachments(self, info):
        return Attachment.objects.all()

    # Pobieranie wszystkich budżetów
    def resolve_all_budgets(self, info):
        return Budget.objects.all()

    # Pobieranie wszystkich transakcji cyklicznych
    def resolve_all_recurring_transactions(self, info):
        return RecurringTransaction.objects.all()

    # Pobieranie wszystkich celów
    def resolve_all_goals(self, info):
        return Goal.objects.all()

# class CreateCategory(graphene.Mutation):
#         class Arguments:
#             name = graphene.String(required=True)
#             description = graphene.String()
#
#         category = graphene.Field(CategoryType)
#
#         def mutate(self, info, name, description=None):
#             category = Category.objects.create(name=name, description=description)
#             return CreateCategory(category=category)

class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        user_id = graphene.Int(required=True)  # Dodajemy user_id jako argument

    category = graphene.Field(CategoryType)

    def mutate(self, info, name, description=None, user_id=None):
        user = User.objects.get(id=user_id)  # Pobieramy użytkownika na podstawie user_id
        category = Category.objects.create(name=name, description=description, user=user)
        return CreateCategory(category=category)



class CreateTransaction(graphene.Mutation):
        class Arguments:
            user_id = graphene.Int(required=True)
            category_id = graphene.Int()
            type = graphene.String(required=True)
            amount = graphene.Decimal(required=True)
            date = graphene.String(required=True)
            description = graphene.String()

        transaction = graphene.Field(TransactionType)

        def mutate(self, info, user_id, category_id, type, amount, date, description=None):
            user = User.objects.get(id=user_id)
            category = Category.objects.get(id=category_id) if category_id else None
            transaction = Transaction.objects.create(
                user=user,
                category=category,
                type=type,
                amount=amount,
                date=date,
                description=description
            )
            return CreateTransaction(transaction=transaction)

class CreateGoal(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        target_amount = graphene.Float(required=True)
        deadline = graphene.String(required=True)  # Deadline jako String w mutacji GraphQL
        saved_amount = graphene.Float()

    goal = graphene.Field(GoalType)

    def mutate(self, info, user_id, name, target_amount, deadline, saved_amount=0):
        # Konwertujemy String na Date
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()

        # Konwertujemy target_amount i saved_amount na Decimal
        target_amount_decimal = Decimal(str(target_amount))
        saved_amount_decimal = Decimal(str(saved_amount))

        # Pobieramy użytkownika i tworzymy cel
        user = User.objects.get(id=user_id)
        goal = Goal.objects.create(
            user=user,
            name=name,
            target_amount=target_amount_decimal,  # Używamy Decimal w backendzie
            saved_amount=saved_amount_decimal,  # Używamy Decimal w backendzie
            deadline=deadline_date  # Zapisujemy datę jako Date w backendzie
        )
        return CreateGoal(goal=goal)


class CreateBudget(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        total_amount = graphene.String(required=True)  # Zmieniono na String
        start_date = graphene.String(required=True)
        end_date = graphene.String(required=True)

    budget = graphene.Field(BudgetType)

    def mutate(self, info, user_id, name, total_amount, start_date, end_date):
        user = User.objects.get(id=user_id)

        # Konwersja string na Decimal
        total_amount_decimal = Decimal(total_amount)

        # Konwersja string na Date
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Tworzenie budżetu
        budget = Budget.objects.create(
            user=user,
            name=name,
            total_amount=total_amount_decimal,
            start_date=start_date_obj,
            end_date=end_date_obj
        )
        return CreateBudget(budget=budget)

# class CreateBudget(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.Int(required=True)
#         name = graphene.String(required=True)
#         total_amount = graphene.Float(required=True)
#         start_date = graphene.String(required=True)
#         end_date = graphene.String(required=True)
#
#     budget = graphene.Field(BudgetType)
#
#     def mutate(self, info, user_id, name, total_amount, start_date, end_date):
#         user = User.objects.get(id=user_id)
#         budget = Budget.objects.create(
#             user=user,
#             name=name,
#             total_amount=total_amount,
#             start_date=start_date,
#             end_date=end_date
#         )
#         return CreateBudget(budget=budget)



class CreateRecurringTransaction(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        category_id = graphene.Int()
        type = graphene.String(required=True)
        amount = graphene.Float(required=True)
        interval = graphene.String(required=True)
        start_date = graphene.String(required=True)
        end_date = graphene.String(required=False)

    recurring_transaction = graphene.Field(RecurringTransactionType)

    def mutate(self, info, user_id, category_id, type, amount, interval, start_date, end_date=None):
        user = User.objects.get(id=user_id)
        category = Category.objects.get(id=category_id) if category_id else None
        recurring_transaction = RecurringTransaction.objects.create(
            user=user,
            category=category,
            type=type,
            amount=amount,
            interval=interval,
            start_date=start_date,
            end_date=end_date
        )
        return CreateRecurringTransaction(recurring_transaction=recurring_transaction)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_transaction = CreateTransaction.Field()
    create_budget = CreateBudget.Field()
    create_goal = CreateGoal.Field()
    create_recurring_transaction = CreateRecurringTransaction.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)