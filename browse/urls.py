from django.urls import path
from .views import (index, filter_json, count_json, get_filter_tokens,
                    cash_token, drop_token)


urlpatterns = [
    path('', index, name='index'),
    path('filter/', filter_json, name='filter'),
    path('count/', count_json, name='count'),
    path('get-filter-tokens/', get_filter_tokens, name='get-tokens'),
    path('cash-token/<str:token>/', cash_token, name='cash-token'),
    path('drop-token/<str:token>/', drop_token, name='drop-token'),
]
