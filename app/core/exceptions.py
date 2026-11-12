class BotError(Exception):
    """Базалық қате классы."""


class LimitExceeded(BotError):
    """Free тариф лимиті аяқталды."""


class NotFound(BotError):
    """Дерек табылмады."""
