from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Networks
from . serializers import NetworksSerializer


class NetworksApiV1View(APIView):
    def get_queryset(self):
        qs = Networks.objects.all()
        return qs

    def get(self, *args, **kwargs) -> Response:
        serializer = NetworksSerializer(
            instance=Networks.objects.first(),
            many=False,
            context={'request': self.request},
        )
        return Response(serializer.data)

    def post(self, *args, **kwargs) -> Response:
        networks = Networks.objects.first()

        if not networks:
            serializer = NetworksSerializer(
                data=self.request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return self.patch()

    def patch(self, *args, **kwargs) -> Response:
        networks = Networks.objects.first()
        serializer = NetworksSerializer(
            instance=networks,
            data=self.request.data,
            context={'request': self.request},
            partial=True,
            many=False,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )
