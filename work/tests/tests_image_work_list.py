from django.urls import reverse, resolve
from work import views
from utils.mocks.work import make_image_work, make_work
from utils.mocks.auth import APITestCaseWithLogin


class WorkImagesListAPIV1ViewTests(APITestCaseWithLogin):
    url = reverse('works:image-list', args=(1,))

    def test_work_images_list_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/api/images/1/list/'
        )

    def test_work_images_list_uses_correct_view(self) -> None:
        response = resolve(self.url)

        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkImagesListAPIView,
        )

    def test_work_images_list_returns_status_code_404_if_no_work(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_work_images_list_returns_status_code_200_if_work(self) -> None:
        work = make_work()
        make_image_work(work_instance=work, num_of_imgs=1)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_work_images_list_returns_correct_content(self) -> None:
        work = make_work()
        make_image_work(work_instance=work, num_of_imgs=3)

        response = self.client.get(self.url)

        self.assertEqual(
            len(response.data),  # type: ignore
            3,
        )
