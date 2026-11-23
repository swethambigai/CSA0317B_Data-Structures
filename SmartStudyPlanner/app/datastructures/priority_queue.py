"""
SmartStudyPlanner - Priority Queue

Data Structure:
    Priority Queue

Purpose:
    Organizes study topics according to importance.

Priority is calculated using:
    - Topic difficulty
    - Urgency
    - Deadline
    - Revision status

Higher priority means the topic should be studied earlier.
"""


class PriorityQueue:
    """Priority queue for intelligent study scheduling."""

    def __init__(self):
        self.items = []

    def calculate_priority(self, topic):
        """
        Calculate the priority of a topic.

        Expected topic format:

        {
            "name": "Binary Trees",
            "difficulty": "Hard",
            "urgency": 4,
            "deadline_days": 2,
            "revision_due": True
        }

        Higher number = higher priority.
        """

        if not isinstance(topic, dict):
            return 0

        priority = 0

        # ---------------------------------------------
        # DIFFICULTY
        # ---------------------------------------------

        raw_difficulty = topic.get(
            "difficulty",
            "Medium"
        )
        difficulty_str = str(raw_difficulty).lower().strip()

        difficulty_scores = {
            "1": 1,
            "easy": 1,
            "2": 2,
            "medium": 2,
            "moderate": 2,
            "3": 4,
            "hard": 4,
            "critical": 5
        }

        priority += difficulty_scores.get(
            difficulty_str,
            2
        )

        # ---------------------------------------------
        # EXPLICIT TOPIC PRIORITY (IF PROVIDED)
        # ---------------------------------------------
        topic_prio = topic.get("priority")
        if topic_prio is not None:
            try:
                p_val = int(topic_prio)
                # Map 1-3 priority or raw integer to priority boost
                priority += p_val * 2
            except (TypeError, ValueError):
                pass

        # ---------------------------------------------
        # URGENCY
        # ---------------------------------------------

        urgency = topic.get(
            "urgency",
            0
        )

        try:
            urgency = int(urgency)
        except (TypeError, ValueError):
            urgency = 0

        urgency = max(
            0,
            min(urgency, 5)
        )

        priority += urgency

        # ---------------------------------------------
        # DEADLINE
        # ---------------------------------------------

        deadline_days = topic.get(
            "deadline_days"
        )

        if deadline_days is not None:

            try:
                deadline_days = int(
                    deadline_days
                )

                if deadline_days <= 1:

                    priority += 5

                elif deadline_days <= 3:

                    priority += 3

                elif deadline_days <= 7:

                    priority += 1

            except (TypeError, ValueError):

                pass

        # ---------------------------------------------
        # REVISION DUE
        # ---------------------------------------------

        if topic.get(
            "revision_due",
            False
        ):

            priority += 4

        return priority

    def enqueue(
        self,
        topic,
        priority=None
    ):
        """
        Add a topic to the priority queue.

        If priority is not supplied,
        it is calculated automatically.
        """

        if topic is None:
            raise ValueError(
                "Topic cannot be empty."
            )

        if priority is None:

            priority = self.calculate_priority(
                topic
            )

        entry = {
            "topic": topic,
            "priority": priority
        }

        self.items.append(entry)

        self._sort()

    def _sort(self):
        """Sort from highest priority to lowest."""

        self.items.sort(
            key=lambda item: item["priority"],
            reverse=True
        )

    def dequeue(self):
        """
        Remove and return the highest-priority topic.
        """

        if self.is_empty():
            return None

        entry = self.items.pop(0)

        return entry["topic"]

    def peek(self):
        """
        Return the highest-priority topic
        without removing it.
        """

        if self.is_empty():
            return None

        return self.items[0]["topic"]

    def peek_priority(self):
        """Return the highest priority value."""

        if self.is_empty():
            return None

        return self.items[0]["priority"]

    def is_empty(self):
        """Check whether the priority queue is empty."""

        return len(self.items) == 0

    def size(self):
        """Return the number of topics."""

        return len(self.items)

    def remove(self, topic):
        """Remove a specific topic."""

        for index, item in enumerate(self.items):

            if item["topic"] == topic:

                self.items.pop(index)

                return True

        return False

    def update_priorities(self):
        """
        Recalculate all priorities.

        Useful when:
        - deadline changes
        - revision becomes due
        - difficulty changes
        - urgency changes
        """

        for item in self.items:

            item["priority"] = (
                self.calculate_priority(
                    item["topic"]
                )
            )

        self._sort()

    def get_all(self):
        """
        Return all topics with their priorities.
        """

        return [
            {
                "topic": item["topic"],
                "priority": item["priority"]
            }
            for item in self.items
        ]

    def display(self):
        """Return priority queue as readable text."""

        if self.is_empty():
            return "Priority Queue is empty."

        result = []

        for index, item in enumerate(
            self.items,
            start=1
        ):

            topic = item["topic"]

            if isinstance(topic, dict):

                name = topic.get(
                    "name",
                    "Unnamed Topic"
                )

            else:

                name = str(topic)

            result.append(
                f"{index}. {name} "
                f"(Priority: {item['priority']})"
            )

        return "\n".join(result)

    def __len__(self):
        """Allow len(priority_queue)."""

        return len(self.items)

    