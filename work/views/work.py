from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from work.models import Work
from work.serializers import WorkSerializer


class WorkCreateDetailAPIV1View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

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


class WorkListAPIV1View(APIView):
    http_method_names = ['get']

    def get_queryset(self) -> list[Work]:
        qs = Work.objects.all()
        return qs  # type: ignore

    def get(self, *args, **kwargs) -> Response:
        works = self.get_queryset()

        serializer = WorkSerializer(
            instance=works,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
