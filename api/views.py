from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from api.filters import InStockFilterBackend, ProductFilter
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import (
IsAuthenticated, IsAdminUser, AllowAny
)
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination 

class ProductListAPIView(generics.ListAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView): 
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       InStockFilterBackend
                       ]
    search_fields = ['name','description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = LimitOffsetPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 6 
    
    def get_permissions(self): 
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST': 
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductCreateAPIView(generics.CreateAPIView): 
    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs): 
        print(request.data)
        return super().create(request, *args, **kwargs)

# @api_view(['GET'])
# def product_list(request): 
#     products = Product.objects.all() 
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg='product_id'

    def get_permissions(self): 
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']: 
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
# @api_view(['GET'])
# def product_detail(request, pk): 
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet): 
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None 

# class OrderListAPIView(generics.ListAPIView): 
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
    
    
# class UserOrderListAPIView(generics.ListAPIView): 
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self): 
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
    
# @api_view(['GET'])
# def order_list(request): 
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class ProductInfoAPIView(APIView): 
    def get(self, request): 
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)

# @api_view(['GET'])
# def product_info(request): 
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)