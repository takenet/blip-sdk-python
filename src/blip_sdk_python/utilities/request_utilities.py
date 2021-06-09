from urllib.parse import quote


class RequestUtilities:
    """Requests utilities."""

    @staticmethod
    def quote(
        uri: str,
        *args
    ) -> str:
        """Url Encode.

        Args:
            uri (str): uri to encode
            args: urllib.parse.quote original args

        Returns:
            str: encoded uri
        """  # noqa: DAR101
        return quote(uri, *args).replace('%24', '$').replace('%27', "'")
