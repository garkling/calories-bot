from enum import Enum, auto

from telethon.tl.custom import Message


class States(Enum):
    WAIT_WEIGHT = auto()
    WAIT_SEARCH = auto()


class StateChecker:

    def __init__(self):
        self.current_product = {}
        self.conversation_states = {}

    def del_state(self, user_id):
        if user_id in self.conversation_states:
            del self.conversation_states[user_id]
        else:
            return False

    def set_product(self, user_id, product_id):
        self.current_product[user_id] = product_id

    def set_state(self, user_id, state=States.WAIT_SEARCH):
        self.conversation_states[user_id] = state

    def check_state(self, state):

        def decorator(f):
            async def wrapper(event: Message):
                user_id = event.sender_id
                user_state = self.conversation_states.get(user_id)

                if user_state != state:
                    if user_state is not None:
                        self.set_state(user_id)
                    else:
                        return

                await f(event)

            return wrapper
        return decorator
