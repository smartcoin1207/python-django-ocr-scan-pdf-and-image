from django_filters import rest_framework as filters

# from core.models import ChatSession

# class SessionFilter(filters.FilterSet):
#     chatbot = filters.CharFilter(field_name='chatbot__id', lookup_expr='iexact')
#     helpful = filters.BooleanFilter(field_name='is_response_helpful')
#     start = filters.DateFilter(field_name='created_at', lookup_expr='gte')
#     end = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    # class Meta:
    #     model = ChatSession
    #     fields = ('chatbot', 'is_response_helpful', 'start', 'end')