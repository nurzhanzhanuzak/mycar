from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchVector
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.settings import api_settings
from cars.serializers import CarSerializer
from cars.models import Car


class CarViewSet(ViewSet):

    def list(self, request):
        queryset = Car.objects.order_by('pk')
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Car.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CarSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=404)
        serializer = CarSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


@api_view(('GET',))
@renderer_classes(api_settings.DEFAULT_RENDERER_CLASSES)
def search(request):
    maybe_search_query = request.GET.urlencode().split('=')
    if 'search' not in maybe_search_query or maybe_search_query[0] != 'search':
        return Response(status=400)
    query = maybe_search_query[1]
    if not query:
        return Response(status=400)
    search_vector = SearchVector('make', 'model', 'price', 'year', 'mileage')
    search_query = SearchQuery(query, search_type='websearch')
    queryset = Car.objects.annotate(
        search=search_vector
    ).filter(search=search_query)
    serializer = CarSerializer(queryset, many=True)
    return Response(serializer.data)
