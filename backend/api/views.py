from rest_framework.authentication import  TokenAuthentication
from rest_framework.views import APIView

from api.parsers import XMLDocRenderer
from .paginations import CustomPagination
from rest_framework.response import Response
from rest_framework import  permissions


class PaginationAPIView(APIView):
    '''
    APIView with pagination
    '''
    pagination_class = CustomPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    
class XMLParserView(APIView):
    renderer_classes = (XMLDocRenderer,)
    #authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]
    
    def post(self,request):
        return Response(request.data)