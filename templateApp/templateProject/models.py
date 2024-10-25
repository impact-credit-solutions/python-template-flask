from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from knox.auth import TokenAuthentication
from nanoid import generate as nano_generate
from rest_framework import filters, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class Case(models.Model):

    case_id = models.CharField(default=nano_generate, primary_key=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    field_custom = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    updated_at = models.DateTimeField(auto_now=True)


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        # fields = ["case_id", "sources", "description"]
        # fields = "__all__"
        exclude = ["user"]


class CaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = CaseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["description"]
    search_fields = ["description"]
    ordering_fields = ["created_at", "description"]
    ordering = ["created_at"]
    queryset = Case.objects.all()

    # def get_queryset(self):
    #     request = self.request
    #     abstract = request.user

    #     case_by_user: models.BaseManager[Case] = Case.objects.filter(users=abstract.id)

    #     return case_by_user.all()
