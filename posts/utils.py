def is_not_authenticated(request) -> bool:
    """Check if the user is not authenticated."""
    return not request.user.is_authenticated


def is_superuser(request) -> bool:
    """Check if the user is a superuser."""
    return request.user.is_superuser


def is_author(post, request) -> bool:
    """Check if the user is the author of the post."""
    return request.user == post.author
