from utils.mocks.auth import APITestCaseWithLogin
from django.urls import reverse, resolve
from work import views
from utils.mocks.work import make_work, make_image_work


class WorkApiV1Tets(APITestCaseWithLogin):
    url = reverse('works:work', args=('work-title',))

    def test_work_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/work-title/',
        )

    def test_work_uses_correct_view(self) -> None:
        response = resolve(self.url)

        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkAPIV1View,
        )

    def test_work_returns_status_code_404_if_not_work(self) -> None:
        response = self.client.get(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_work_returns_status_code_200_if_work(self) -> None:
        # create an work
        work = make_work()
        make_image_work(work_instance=work, num_of_imgs=3)

        response = self.client.get(
            self.url,
        )

        print(response.data)

        self.assertEqual(
            response.status_code,
            200,
        )
