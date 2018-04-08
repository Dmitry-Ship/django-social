class Error(Exception):
    pass


class AlreadyLiked(Error):
    def __str__(str):
        return 'You already liked it'

