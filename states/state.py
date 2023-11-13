from abc import ABC

class State(ABC):
    """Represents a state"""

    def set_context(self, context):
        """sets the context for the state"""
        self._context = context

    def get_context(self):
        """Returns the state's context"""
        return self._context

