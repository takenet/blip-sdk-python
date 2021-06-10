from pytest import mark
from src.blip_sdk.utilities import RequestUtilities


class TestRequestUtilities:

    @mark.parametrize(
        ['input', 'expected_result'],
        [
            ('foo bar', 'foo%20bar'),  # noqa: WPS323
            ('$take', '$take')
        ]
    )
    def test_quote(self, input: str, expected_result: str) -> None:
        # Act
        result = RequestUtilities.quote(input)

        # Assert
        assert result == expected_result
