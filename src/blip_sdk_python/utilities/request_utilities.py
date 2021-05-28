from urllib.parse import quote


class RequestUtilities:
    """Requests utilities."""

    @staticmethod
    def quote(
        uri: str,
        safe: str = None,
        encoding: str = None,
        errors: str = None
    ) -> str:
        """Url Encode.

        Args:
            uri (str): uri to encode

        Returns:
            str: encoded uri
        """  # noqa: DAR101
        return quote(uri).replace('%24', '$')
