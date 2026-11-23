
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app.datastructures.queue import StudyQueue


def test_queue_creation():
    queue = StudyQueue()

    assert queue.is_empty()


def test_enqueue():
    queue = StudyQueue()

    queue.enqueue("Mathematics")

    assert not queue.is_empty()
    assert queue.size() == 1


def test_dequeue():
    queue = StudyQueue()

    queue.enqueue("Mathematics")
    queue.enqueue("Physics")

    first_topic = queue.dequeue()

    assert first_topic == "Mathematics"
    assert queue.size() == 1


def test_fifo_behavior():
    queue = StudyQueue()

    queue.enqueue("Topic 1")
    queue.enqueue("Topic 2")
    queue.enqueue("Topic 3")

    assert queue.dequeue() == "Topic 1"
    assert queue.dequeue() == "Topic 2"
    assert queue.dequeue() == "Topic 3"


def test_peek():
    queue = StudyQueue()

    queue.enqueue("Data Structures")

    assert queue.peek() == "Data Structures"
    assert queue.size() == 1


def test_empty_dequeue():
    queue = StudyQueue()

    assert queue.dequeue() is None

