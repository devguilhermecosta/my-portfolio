from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from work.models import Work
from work.serializers import WorkSerializer


class WorkDetailAPIV1View(APIView):
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


# criar a view para a list de trabalhos
