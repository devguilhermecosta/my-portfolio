from work.models import Work, WorkImage
from utils.mocks.images import make_simple_image


def make_work(title: str | None = None) -> Work:
    obj = Work.objects.create(
        title='Work Title' or title,
        slug='work-title',
        description='this the the description',
        link='https://my-work.com',
        cover=make_simple_image(),
    )
    obj.save()
    return obj


def make_image_work(work_instance: Work | None = None,
                    num_of_imgs: int = 1,
                    ) -> tuple[Work, list[WorkImage]]:
    work = work_instance or make_work()

    images = []

    for _ in range(num_of_imgs):
        image = WorkImage.objects.create(
            work=work,
            image=make_simple_image(),
        )
        image.save()
        images.append(image)

    return work, images
