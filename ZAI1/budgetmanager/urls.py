from django.urls import path
from . import views
urlpatterns = [
    path('', views.ApiRoot.as_view(), name='api-root'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('token/refresh/', views.TokenRefreshAPIView.as_view(), name='token_refresh'),

  # User endpoints
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # Category endpoints
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Transaction endpoints
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),

    # Attachment endpoints
    path('attachments/', views.AttachmentListView.as_view(), name='attachment-list'),
    path('attachments/<int:pk>/', views.AttachmentDetailView.as_view(), name='attachment-detail'),

    # Budget endpoints
    path('budgets/', views.BudgetListView.as_view(), name='budget-list'),
    path('budgets/<int:pk>/', views.BudgetDetailView.as_view(), name='budget-detail'),

    # RecurringTransaction endpoints
    path('recurring-transactions/', views.RecurringTransactionListView.as_view(), name='recurring-transaction-list'),
    path('recurring-transactions/<int:pk>/', views.RecurringTransactionDetailView.as_view(), name='recurring-transaction-detail'),

    # Goal endpoints
    path('goals/', views.GoalListView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal-detail'),
]
