from django.urls import path
from .views import (
    CreateStringView,
    StringDetailView,
    FilterByNaturalLanguageView,
)

urlpatterns = [
    path('strings/', CreateStringView.as_view(), name='create_or_list_strings'),
    path('strings/filter-by-natural-language', FilterByNaturalLanguageView.as_view(), name='nl_filter'),
    path('strings/<str:string_value>', StringDetailView.as_view(), name='string_detail'),
]
