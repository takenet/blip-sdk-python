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
            data.update(vars(entry))  # noqa: WPS421

        return args[-1].__class__(**data)
