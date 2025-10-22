from django.urls import path
from .views import (
    CreateStringView,
    StringDetailView,
    ListStringsView,
    FilterByNaturalLanguageView,
)

# Important: put specific routes BEFORE the dynamic <str:string_value> route
urlpatterns = [
    # support both with and without trailing slash for POST & GET list
    path('strings', CreateStringView.as_view(), name='create_or_list_strings_no_slash'),
    path('strings/', CreateStringView.as_view(), name='create_or_list_strings'),

    # natural language filter (both forms)
    path('strings/filter-by-natural-language', FilterByNaturalLanguageView.as_view(), name='nl_filter_no_slash'),
    path('strings/filter-by-natural-language/', FilterByNaturalLanguageView.as_view(), name='nl_filter'),

    # list-by-filters route (if you want an explicit list endpoint separate from create)
    path('strings/list', ListStringsView.as_view(), name='list_strings_no_slash'),
    path('strings/list/', ListStringsView.as_view(), name='list_strings'),

    # finally the dynamic detail route (must be last)
    path('strings/<str:string_value>', StringDetailView.as_view(), name='string_detail_no_slash'),
    path('strings/<str:string_value>/', StringDetailView.as_view(), name='string_detail'),
]
