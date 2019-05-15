from rest_framework import permissions
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from .permissions import IsOwnerOrReadonly
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

