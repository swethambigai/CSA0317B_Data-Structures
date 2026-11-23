"""
SmartStudyPlanner - Study Queue

Data Structure:
    Queue (FIFO - First In, First Out)

Purpose:
    Stores study topics waiting to be studied.

Project usage:
    - New topics are added to the rear.
    - The next topic is taken from the front.
    - Difficult topics can be postponed during
      Health Maintenance Mode.
"""


class StudyQueue:
    """FIFO queue for managing study topics."""

    def __init__(self):
        self.items = []

    def enqueue(self, topic):
        """Add a topic to the rear of the queue."""

        if topic is None:
            raise ValueError("Topic cannot be empty.")

        self.items.append(topic)

    def dequeue(self):
        """Remove and return the topic at the front."""

        if self.is_empty():
            return None

        return self.items.pop(0)

    def front(self):
        """Return the first topic without removing it."""

        if self.is_empty():
            return None

        return self.items[0]

    def peek(self):
        """Return the first topic without removing it (alias for front)."""

        return self.front()

    def rear(self):
        """Return the last topic without removing it."""

        if self.is_empty():
            return None

        return self.items[-1]

    def is_empty(self):
        """Check whether the queue is empty."""

        return len(self.items) == 0

    def size(self):
        """Return the number of topics."""

        return len(self.items)

    def clear(self):
        """Remove all topics from the queue."""

        self.items.clear()

    def move_to_end(self, topic):
        """
        Move a topic to the end of the queue.

        Used when a topic needs to be postponed.
        """

        if topic in self.items:
            self.items.remove(topic)
            self.items.append(topic)
            return True

        return False

    def postpone_difficult_topics(self):
        """
        Move hard and critical topics to the end.

        Expected topic format:

        {
            "name": "Data Structures",
            "difficulty": "Hard"
        }
        """

        normal_topics = []
        difficult_topics = []

        for topic in self.items:

            if isinstance(topic, dict):

                difficulty = str(
                    topic.get("difficulty", "")
                ).lower()

            else:

                difficulty = ""

            if difficulty in ("hard", "critical"):

                difficult_topics.append(topic)

            else:

                normal_topics.append(topic)

        self.items = (
            normal_topics +
            difficult_topics
        )

    def get_all(self):
        """Return a copy of all queue items."""

        return self.items.copy()

    def display(self):
        """Return the queue as readable text."""

        if self.is_empty():
            return "Study Queue is empty."

        result = []

        for index, topic in enumerate(
            self.items,
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
        """Allow len(queue)."""

        return len(self.items)

    def __iter__(self):
        """Allow iteration through the queue."""

        return iter(self.items)