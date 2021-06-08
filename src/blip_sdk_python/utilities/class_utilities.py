from typing import Any


class ClassUtilities:
    """Classes utilities."""

    @staticmethod
    def merge_dataclasses(*args) -> Any:
        """Merge two or more dataclasses.

        Adapted solution from:
        https://stackoverflow.com/questions/9667818/python-how-to-merge-two-class

        Args:
            args: dataclasses to merge

        Raises:
            ValueError: dataclasses of different types were passed

        Returns:
            Any: the merged dataclass
        """
        if len({arg.__class__.__name__ for arg in args}) > 1:
            raise ValueError(
                'Merge of non-homogeneous entries no allowed.'
            )
        data = {}
        for entry in args:
            data.update(
                ClassUtilities.__remove_none_values(
                    vars(entry)  # noqa: WPS421
                )
            )

        return args[-1].__class__(**data)

    @staticmethod
    def __remove_none_values(data: dict) -> dict:
        clear_data: dict = {}
        for key, value in data.items():
            if value is not None:
                clear_data[key] = value
        return clear_data
