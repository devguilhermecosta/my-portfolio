from work.models import Work, WorkImage
from utils.mocks.images import make_simple_image


def make_work(title: str | None = None,
              slug: str | None = None,
              description: str | None = None,
              link: str | None = None,
              ) -> Work:
    obj = Work.objects.create(
        title=title or 'Work Title',
        slug=slug or 'work-title',
        description=description or 'this is the the description',
        link=link or 'https://my-work.com',
        cover=make_simple_image(),
    )
    obj.save()
    return obj


def make_work_in_batch(num_of_works: int = 1,
                       with_images: bool = False,
                       num_of_images_per_obj: int = 1,
                       ) -> list[Work]:
    works = []

    for i in range(num_of_works):
        new_work = make_work(
            title=f'work title - num {i}',
            slug=f'work-title-{i}'
            )
        if with_images:
            for i in range(num_of_images_per_obj):
                make_image_work(work_instance=new_work)
        works.append(new_work)

    return works


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
