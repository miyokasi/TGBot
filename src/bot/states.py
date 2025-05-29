from telegram.ext import ConversationHandler

from .questions import QUESTION_FLOW


STATE_KEYS = [q[0] for q in QUESTION_FLOW]
STATE_ORDER = list(range(len(STATE_KEYS)))
STATE_MAP = dict(zip(STATE_ORDER, STATE_KEYS))
REVERSE_STATE_MAP = {v: k for k, v in STATE_MAP.items()}

EDITING = 99


def end():
    return ConversationHandler.END
