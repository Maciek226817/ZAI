from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Transaction, Attachment, Budget, RecurringTransaction, Goal
from django.core.files.uploadedfile import SimpleUploadedFile

class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.category = Category.objects.create(
            name='Groceries',
            description='Monthly groceries expenses',
            user=self.user
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Groceries')
        self.assertEqual(self.category.description, 'Monthly groceries expenses')
        self.assertEqual(self.category.user, self.user)
        self.assertEqual(str(self.category), 'Groceries')

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='password')
        self.category = Category.objects.create(name='Utilities', user=self.user)
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            type='expense',
            amount=150.75,
            date='2025-04-01',
            description='Electricity bill'
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.type, 'expense')
        self.assertEqual(self.transaction.amount, 150.75)
        self.assertEqual(self.transaction.category, self.category)
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(str(self.transaction), 'Expense - 150.75 (2025-04-01)')

class AttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user3', password='password')
        self.category = Category.objects.create(name='Entertainment', user=self.user)
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            type='income',
            amount=300.00,
            date='2025-04-02',
            description='Refund'
        )
        self.attachment = Attachment.objects.create(
            transaction=self.transaction,
            file=SimpleUploadedFile("receipt.pdf", b"file_content")
        )

    def test_attachment_creation(self):
        self.assertEqual(self.attachment.transaction, self.transaction)
        self.assertEqual(str(self.attachment), f'Attachment for {self.transaction}')

class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user4', password='password')
        self.budget = Budget.objects.create(
            user=self.user,
            name='Monthly Budget',
            total_amount=2000.00,
            start_date='2025-04-01',
            end_date='2025-04-30'
        )

    def test_budget_creation(self):
        self.assertEqual(self.budget.name, 'Monthly Budget')
        self.assertEqual(self.budget.total_amount, 2000.00)
        self.assertEqual(self.budget.user, self.user)
        self.assertEqual(str(self.budget), 'Budget: Monthly Budget (2025-04-01 - 2025-04-30)')

class RecurringTransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user5', password='password')
        self.category = Category.objects.create(name='Rent', user=self.user)
        self.recurring_transaction = RecurringTransaction.objects.create(
            user=self.user,
            category=self.category,
            type='expense',
            amount=800.00,
            interval='monthly',
            start_date='2025-01-01',
            end_date='2025-12-31'
        )

    def test_recurring_transaction_creation(self):
        self.assertEqual(self.recurring_transaction.amount, 800.00)
        self.assertEqual(self.recurring_transaction.interval, 'monthly')
        self.assertEqual(self.recurring_transaction.user, self.user)
        self.assertEqual(str(self.recurring_transaction), 'Recurring Expense - 800.0 (monthly)')

class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user6', password='password')
        self.goal = Goal.objects.create(
            user=self.user,
            name='Vacation Fund',
            target_amount=3000.00,
            saved_amount=500.00,
            deadline='2025-12-31'
        )

    def test_goal_creation(self):
        self.assertEqual(self.goal.name, 'Vacation Fund')
        self.assertEqual(self.goal.target_amount, 3000.00)
        self.assertEqual(self.goal.saved_amount, 500.00)
        self.assertEqual(self.goal.deadline, '2025-12-31')
        self.assertEqual(str(self.goal), 'Goal: Vacation Fund (Target: 3000.0, Saved: 500.0)')