"""
SmartStudyPlanner - Revision Stack

Data Structure:
    Stack (LIFO - Last In, First Out)

Purpose:
    Stores recently completed topics.

Project usage:
    - Completed topics are pushed onto the stack.
    - The most recently completed topic is accessed first.
    - Used for quick revision.
    - Health Maintenance Mode can limit the number
      of revision topics available.
"""


class RevisionStack:
    """LIFO stack for revision topics."""

    def __init__(self, max_size=None):
        self.items = []
        self.max_size = max_size

    def push(self, topic):
        """
        Add a topic to the top of the stack.

        Returns:
            True if successfully added.
            False if the stack is full.
        """

        if topic is None:
            raise ValueError("Topic cannot be empty.")

        if (
            self.max_size is not None
            and len(self.items) >= self.max_size
        ):
            return False

        self.items.append(topic)

        return True

    def pop(self):
        """Remove and return the top topic."""

        if self.is_empty():
            return None

        return self.items.pop()

    def peek(self):
        """Return the top topic without removing it."""

        if self.is_empty():
            return None

        return self.items[-1]

    def is_empty(self):
        """Check whether the stack is empty."""

        return len(self.items) == 0

    def size(self):
        """Return the number of topics."""

        return len(self.items)

    def clear(self):
        """Remove all topics."""

        self.items.clear()

    def health_mode_limit(self, limit=2):
        """
        Return only the most recent revision topics.

        Health Maintenance Mode uses this to limit
        the student's revision workload.
        """

        if limit < 1:
            limit = 1

        return self.items[-limit:]

    def complete_revision(self):
        """
        Complete the current revision topic.

        The top topic is removed from the stack.
        """

        return self.pop()

    def get_all(self):
        """
        Return all topics from top to bottom.
        """

        return list(
            reversed(self.items)
        )

    def display(self):
        """Return stack contents as readable text."""

        if self.is_empty():
            return "Revision Stack is empty."

        result = []

        for index, topic in enumerate(
            reversed(self.items),
            start=1
        ):

            if isinstance(topic, dict):

                name = topic.get(
                    "name",
                    "Unnamed Topic"
                )

            else:

                name = str(topic)

            result.append(
                f"{index}. {name}"
            )

        return "\n".join(result)

    def __len__(self):
        """Allow len(stack)."""

        return len(self.items)

    def __iter__(self):
        """Iterate from top to bottom."""

        return reversed(self.items)