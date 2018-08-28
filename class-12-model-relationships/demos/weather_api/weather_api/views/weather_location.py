from ..models.schemas import WeatherLocationSchema
from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.response import Response
from pyramid.view import view_config
from ..models import WeatherLocation
import requests
import json
import os


@view_config(route_name='lookup', renderer='json', request_method='GET')
def lookup(request):
    """
    """
    url = '{}/weather?zip={}&APPID={}'.format(
        os.environ.get('API_URL'),
        request.matchdict['zip'],
        os.environ.get('API_KEY'),
    )
    res = requests.get(url)

    return Response(json=res.json(), status=200)


class WeatherLocationAPIView(APIViewSet):
    def create(self, request):
        """
        """
        try:
            kwargs = json.loads(request.body)
        except json.JSONDecodeError as e:
            return Response(json=e.msg, status=400)

        if 'zip_code' not in kwargs:
            return Response(json='Expected value; zip_code')

        try:
            weather = WeatherLocation.new(request=request, **kwargs)
        except IntegrityError:
            return Response(json='Conflict. Zip code already exists.', status=409)

        schema = WeatherLocationSchema()
        data = schema.dump(weather).data

        return Response(json=data, status=201)

    def list(self, request):
        """
        """
        records = WeatherLocation.all(request)
        schema = WeatherLocationSchema()
        data = [schema.dump(record).data for record in records]

        return Response(json=data, status=200)

    def retrieve(self, request, id=None):
        """
        """
        record = WeatherLocation.one(request=request, pk=id)
        if not record:
            return Response(json='No Found', status=400)

        schema = WeatherLocationSchema()
        data = schema.dump(record).data

        return Response(json=data, status=200)

    def destroy(self, request, id=None):
        """
        """
        if not id:
            return Response(json='Bad Request', status=400)

        try:
            WeatherLocation.remove(request=request, pk=id)
        except (DataError, AttributeError):
            return Response(json='Not Found', status=404)

        return Response(status=204)
