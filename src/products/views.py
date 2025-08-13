from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Product 
from .serializers import ProductSerializer 
from .tasks import notify_product_change
from .tasks import save_visualization_metrics 

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        qs = Product.objects.all().order_by('-created_at')
        if not self.request.user.is_authenticated:
            qs = qs.filter(visible=True)
        return qs

    def perform_update(self, serializer):
        instance = self.get_object()
        old = {
            "name": instance.name,
            "sku": instance.sku,
            "price": instance.price,
            "visible": instance.visible,
            "brand": instance.brand,
        }
        new = serializer.save()
        changes = {}
        for key in old.keys():
            new_value = getattr(new, key)
            if new_value != old[key]:
                changes[key] = [old[key], new_value]

        if not changes:
            return 

        transaction.on_commit(lambda: notify_product_change.delay(new.id, changes, self.request.user.id)) 

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if not page:
            serializer = self.get_serializer(queryset, many=True)
            try:
                products = list(queryset.values_list("pk", flat=True))
                save_visualization_metrics.delay(
                    products,
                    ip=request.META.get("REMOTE_ADDR"),
                    user_agent=request.META.get("HTTP_USER_AGENT"),
                )
            except Exception:
                pass
            return Response(serializer.data)

        serializer = self.get_serializer(page, many=True)

        try:
            products = [obj.id for obj in page]
            save_visualization_metrics.delay(
                products,
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
        except Exception:
            pass

        return self.get_paginated_response(serializer.data)