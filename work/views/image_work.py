from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import Http404
from work.models import WorkImage
from work.serializers import WorkImageSerializer


class WorkImagesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_images_or_404(self, id: int | None) -> list[WorkImage]:
        qs = WorkImage.objects.filter(
            work_id=id,
        )

        if not qs:
            raise Http404()

        return qs  # type: ignore

    def get_queryset(self, *args, **kwargs) -> list[WorkImage] | None:
        qs = WorkImage.objects.all()
        return qs  # type: ignore

    def get(self, *args, **kwargs) -> Response:
        pk = kwargs.get('id')

        images = self.get_images_or_404(id=pk)

        serializer = WorkImageSerializer(
            instance=images,
            many=True,
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
