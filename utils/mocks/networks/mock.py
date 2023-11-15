from networks.models import Networks


def make_networks() -> Networks:
    """
        make a new instance of Networks
    """
    obj = Networks.objects.create(
        instagram="https://www.instagram.com",
        linkedin="https://www.linkedin.com",
        github="https://www.github.com",
        whatsapp="https://www.whatsapp.com",
        phone="46999083251",
        email="guilherme.partic@gmail.com",
        )
    obj.save()
    return obj
