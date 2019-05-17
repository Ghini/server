from django.urls import path
from .views import index, filter_json, count_json, pay_token, get_filter_tokens


urlpatterns = [
    path('', index, name='index'),
    path('filter/', filter_json, name='filter'),
    path('count/', count_json, name='count'),
    path('get-filter-tokens/', get_filter_tokens, name='get-tokens'),
    path('cash-token/<str:token>/', pay_token, name='cash-token'),
    
]
