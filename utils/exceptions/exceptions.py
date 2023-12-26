class ImageNotFoundError(BaseException):
    def __init__(self, message: str) -> None:
        self.msg = message

    def __str__(self) -> str:
        return self.msg
