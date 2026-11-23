"""
SmartStudyPlanner - Revision Linked List

Data Structure:
    Singly Linked List

Purpose:
    Stores revision history for completed topics.

Project usage:
    - Records every revision cycle.
    - Tracks revision number.
    - Stores the next revision date.
    - Supports spaced repetition.
"""


class RevisionNode:
    """
    A single node in the revision linked list.
    """

    def __init__(
        self,
        topic,
        revision_number=1,
        revision_date=None
    ):

        self.topic = topic

        self.revision_number = (
            revision_number
        )

        self.revision_date = (
            revision_date
        )

        self.next = None


class RevisionLinkedList:
    """
    Singly linked list for revision history.
    """

    def __init__(self):

        self.head = None

        self.tail = None

        self.length = 0

    def append(
        self,
        topic,
        revision_number=1,
        revision_date=None
    ):
        """
        Add a revision record to the end.
        """

        new_node = RevisionNode(
            topic,
            revision_number,
            revision_date
        )

        if self.head is None:

            self.head = new_node

            self.tail = new_node

        else:

            self.tail.next = new_node

            self.tail = new_node

        self.length += 1

        return new_node

    def find_topic(self, topic_name):
        """
        Find all revision records belonging
        to a particular topic.
        """

        current = self.head

        results = []

        while current is not None:

            if isinstance(
                current.topic,
                dict
            ):

                name = current.topic.get(
                    "name",
                    ""
                )

            else:

                name = str(
                    current.topic
                )

            if name == topic_name:

                results.append(
                    current
                )

            current = current.next

        return results

    def get_latest_revision(
        self,
        topic_name
    ):
        """
        Return the most recent revision
        for a topic.
        """

        revisions = self.find_topic(
            topic_name
        )

        if not revisions:
            return None

        return revisions[-1]

    def complete_revision(
        self,
        topic,
        current_cycle,
        revision_date=None
    ):
        """
        Create the next revision cycle.

        Example:

            Cycle 1 -> Cycle 2
            Cycle 2 -> Cycle 3
            Cycle 3 -> Cycle 4
        """

        next_cycle = (
            current_cycle + 1
        )

        return self.append(
            topic,
            next_cycle,
            revision_date
        )

    def get_all(self):
        """
        Return every revision node.
        """

        revisions = []

        current = self.head

        while current is not None:

            revisions.append(
                current
            )

            current = current.next

        return revisions

    def count(self):
        """Return total number of revision records."""

        return self.length

    def delete_first(self):
        """
        Delete the first node and return it.
        """

        if self.head is None:
            return None

        removed = self.head

        self.head = self.head.next

        self.length -= 1

        if self.head is None:
            self.tail = None

        removed.next = None

        return removed

    def clear(self):
        """Remove the complete revision history."""

        self.head = None

        self.tail = None

        self.length = 0

    def display(self):
        """
        Display the complete revision history.
        """

        if self.head is None:
            return "Revision history is empty."

        result = []

        current = self.head

        while current is not None:

            if isinstance(
                current.topic,
                dict
            ):

                topic_name = current.topic.get(
                    "name",
                    "Unnamed Topic"
                )

            else:

                topic_name = str(
                    current.topic
                )

            result.append(
                f"{topic_name} - "
                f"Revision "
                f"{current.revision_number}"
            )

            current = current.next

        return "\n".join(result)

    def __iter__(self):
        """Allow iteration through the linked list."""

        current = self.head

        while current is not None:

            yield current

            current = current.next

    def __len__(self):
        """Allow len(linked_list)."""

        return self.length
    