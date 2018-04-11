class Error(Exception):
    pass


class SelfFollowing(Error):
    def __str__(str):
        return 'User cannot follow himself'


class NotFollowing(Error):
    def __str__(str):
        return 'You are not following this user'
