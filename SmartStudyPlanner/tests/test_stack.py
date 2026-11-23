import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app.datastructures.stack import RevisionStack


def test_stack_creation():
    stack = RevisionStack()

    assert stack.is_empty()


def test_push():
    stack = RevisionStack()

    stack.push("Python Basics")

    assert not stack.is_empty()
    assert stack.size() == 1


def test_pop():
    stack = RevisionStack()

    stack.push("Python")
    stack.push("Data Structures")

    top_topic = stack.pop()

    assert top_topic == "Data Structures"
    assert stack.size() == 1


def test_lifo_behavior():
    stack = RevisionStack()

    stack.push("Topic 1")
    stack.push("Topic 2")
    stack.push("Topic 3")

    assert stack.pop() == "Topic 3"
    assert stack.pop() == "Topic 2"
    assert stack.pop() == "Topic 1"


def test_peek():
    stack = RevisionStack()

    stack.push("Revision Topic")

    assert stack.peek() == "Revision Topic"
    assert stack.size() == 1


def test_empty_pop():
    stack = RevisionStack()

    assert stack.pop() is None