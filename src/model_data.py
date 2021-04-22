class PlexUser(object):
    """
    Object representation of a plex user.
    """

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])
