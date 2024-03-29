from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from work.models import Work
from work.serializers import WorkSerializer
from utils.views import CustomAPIView
from rest_framework_api_key.permissions import HasAPIKey


class WorkCreateDetailAPIV1View(CustomAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permissions_per_method = {
        'GET': HasAPIKey,
    }

    def get(self, *args, **kwargs) -> Response:
        work = get_object_or_404(
            Work,
            slug=kwargs.get('slug'),
        )

        serializer = WorkSerializer(
            instance=work,
            many=False,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, *args, **kwargs) -> Response:
        serializer = WorkSerializer(
            data=self.request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, *args, **kwargs) -> Response:
        work = get_object_or_404(
            Work,
            slug=kwargs.get('slug'),
        )

        serializer = WorkSerializer(
            instance=work,
            many=False,
            data=self.request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    def delete(self, *args, **kwargs) -> Response:
        work = get_object_or_404(
            Work,
            slug=kwargs.get('slug'),
        )

        work.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class WorkListAPIV1View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKey]
    http_method_names = ['get']

    def get(self, request: Request, **kwargs) -> Response:
        works = Work.objects.all().order_by('-id')

        serializer = WorkSerializer(
            instance=works,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
