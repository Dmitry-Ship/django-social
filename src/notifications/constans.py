POST_LIKED = 1
POST_COMMENTED = 2
COMMENT_LIKED = 3
FOLLOWED = 4
TYPE_CHOICES = (
    (POST_LIKED, 'Liked post'),
    (POST_COMMENTED, 'Commented post'),
    (COMMENT_LIKED, 'Liked comment'),
    (FOLLOWED, 'Followed')
)