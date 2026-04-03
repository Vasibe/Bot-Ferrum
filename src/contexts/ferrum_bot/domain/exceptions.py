from src.contexts.ferrum_bot.domain.ferrumBotException import FerrumBotException


class ConfigurationException(FerrumBotException):
    pass


class InvalidUserException(FerrumBotException):
    pass


class LoginFailedException(FerrumBotException):
    pass


class ElementNotFoundException(FerrumBotException):
    pass


class NavigationException(FerrumBotException):
    pass


class SessionExpiredException(FerrumBotException):
    pass
