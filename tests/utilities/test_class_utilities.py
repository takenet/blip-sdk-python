from src.blip_sdk_python.utilities import ClassUtilities
from dataclasses import dataclass


class TestClassUtilities:

    def test_merge_dataclasses(self) -> None:
        # Arrange
        part1 = DummyClass('first', 'bar')
        part2 = DummyClass('second')

        # Act
        result: DummyClass = ClassUtilities.merge_dataclasses(part1, part2)

        # Assert
        assert result.id == part2.id
        assert result.key == part1.key


@dataclass
class DummyClass:
    id: str
    key: str = None
