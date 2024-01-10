from rest_framework.response import Response
from rest_framework import status
from . models import Networks
from . serializers import NetworksSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.views import CustomAPIView
from rest_framework_api_key.permissions import HasAPIKey


class NetworksApiV1View(CustomAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    permissions_per_method = {
        'GET': HasAPIKey,
    }

    def get_queryset(self):
        qs = Networks.objects.first()
        return qs

    def get(self, *args, **kwargs) -> Response:
        networks = self.get_queryset()

        if networks:
            serializer = NetworksSerializer(
                instance=networks,
                many=False,
            )
            return Response(serializer.data)

        return Response(
            {
                'data': 'not found'
            },
            status=status.HTTP_404_NOT_FOUND)

    def post(self, *args, **kwargs) -> Response:
        networks = self.get_queryset()

        if not networks:
            serializer = NetworksSerializer(
                data=self.request.data,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=NetworksSerializer(instance=networks).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, *args, **kwargs) -> Response:
        networks = self.get_queryset()

        if not networks:
            return Response(
                {'data': 'not found'},
                status=status.HTTP_404_NOT_FOUND,
                )

        serializer = NetworksSerializer(
            instance=networks,
            data=self.request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_204_NO_CONTENT,
        )
