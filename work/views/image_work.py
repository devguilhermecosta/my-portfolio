from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404, get_list_or_404
from work.models import WorkImage
from work.serializers import WorkImageSerializer
from utils.auth.decorators import token_verify
from django.utils.decorators import method_decorator


@method_decorator(
    token_verify,
    name='get'
)
class WorkImagesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, *args, **kwargs) -> Response:
        image = get_object_or_404(
            WorkImage,
            pk=kwargs.get('id'),
        )

        serializer = WorkImageSerializer(
            instance=image,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, *args, **kwargs) -> Response:
        serializer = WorkImageSerializer(
            data=self.request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, *args, **kwargs) -> Response:
        image = get_object_or_404(
            WorkImage,
            pk=kwargs.get('id')
        )

        serializer = WorkImageSerializer(
            instance=image,
            data=self.request.data,
            many=False,
            partial=True,
        )
        serializer.is_valid(raise_exception=True),
        serializer.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    def delete(self, *args, **kwargs) -> Response:
        image = get_object_or_404(
            WorkImage,
            pk=kwargs.get('id'),
        )

        image.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@method_decorator(
    token_verify,
    name='get'
)
class WorkImagesListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get(self, *args, **kwargs) -> Response:
        images = get_list_or_404(
            WorkImage,
            work_id=kwargs.get('id'),
        )

        serializer = WorkImageSerializer(
            instance=images,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
