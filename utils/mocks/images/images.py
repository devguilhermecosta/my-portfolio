from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
from utils.exceptions import ImageNotFoundError


def make_simple_image() -> SimpleUploadedFile:
    try:
        path = Path(__file__).parent.parent.parent.parent
        img_path = ''.join([
            str(path),
            '/utils/mocks/images/img-test.jpeg',
            ])
        simple_image = SimpleUploadedFile(
            'image_test.jpeg',
            open(img_path, 'rb').read(),
            content_type='image/jpeg',
        )
    except FileNotFoundError:
        raise ImageNotFoundError(f'Path {img_path} not found')

    return simple_image
