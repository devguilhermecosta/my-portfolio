from PIL import Image


def resize_image(image_path: str, image_width: int = 800):
    """
        Resize image maintaining the aspect ratio

        Param image: ImageField
        Param image_width: Image

        return None
    """
    image_open = Image.open(image_path)
    width, height = image_open.size

    ratio_w_h = (height * 100) / width

    if width < image_width:
        return None

    image_height = round((image_width * ratio_w_h) / 100)
    new_image = image_open.resize((image_width, image_height), Image.LANCZOS)

    new_image.save(image_path,
                   optimize=True,
                   quality=100,
                   )

    return new_image
