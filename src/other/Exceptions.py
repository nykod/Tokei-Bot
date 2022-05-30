class IllegalArgumentException(Exception):
    """Raised when there is invalid input in command"""
    """ERR601"""
    pass


class MatchBoxListException(Exception):
    """Raised when there is invalid length of a list"""
    """ERR602"""
    pass


class PlayerNotFoundException(Exception):
    """Raised when there is invalid length of a list"""
    """ERR603"""
    pass


class WebSiteNotFoundException(Exception):
    """Raised when website throws 404 err"""
    """ERR604"""
    pass


class PlayerEloException(Exception):
    """Raised when players elo has wrong value"""
    """ERR605"""
    pass


class NoMapsException(Exception):
    """Raised when team has no maps in last 3 months. Main using is in only one method"""
    """ERR606"""
    pass


class NoOngoingMatchesException(Exception):
    """Raised when there are no any matches ongoing"""
    """ERR607"""
    pass
