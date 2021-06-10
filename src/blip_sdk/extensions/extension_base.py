from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict
from urllib.parse import urlencode
from uuid import uuid4

from lime_python import Command, CommandMethod

from ..utilities import RequestUtilities

if TYPE_CHECKING:
    from ..client import Client


class ExtensionBase:
    """Class base to all sdk extensions."""

    def __init__(self, client: Client, to: str = None) -> None:
        self.client = client
        self.to = to

    def create_get_command(
        self,
        uri: str,
        id: str = None
    ) -> Command:
        """Create a get Command.

        Args:
            uri (str): Command uri
            id (str): Comand id

        Returns:
            Command
        """
        command = Command(CommandMethod.GET, uri)
        command.id = id if id else str(uuid4())

        if self.to:
            command.to = self.to

        return command

    def create_set_command(
        self,
        uri: str,
        resource: Any,
        type_n: str = None,
        id: str = None
    ) -> Command:
        """Create a set Command.

        Args:
            uri (str): Command uri
            type_n (str): resource mime type
            resource (Any): Command resource
            id (str): Command id

        Returns:
            Command
        """
        command = Command(CommandMethod.SET, uri, type_n, resource)
        command.id = id if id else str(uuid4())

        if self.to:
            command.to = self.to

        return command

    def create_merge_command(
        self,
        uri: str,
        resource: Any,
        type_n: str = None,
        id: str = None
    ) -> Command:
        """Create a merge Command.

        Args:
            uri (str): Command uri
            type_n (str): resource mime type
            resource (Any): Command resource
            id (str): Command id

        Returns:
            Command
        """
        command = Command(CommandMethod.MERGE, uri, type_n, resource)
        command.id = id if id else str(uuid4())

        if self.to:
            command.to = self.to

        return command

    def create_delete_command(
        self,
        uri: str,
        id: str = None
    ) -> Command:
        """Create a delete Command.

        Args:
            uri (str): Command uri
            id (str): Command id

        Returns:
            Command
        """
        command = Command(CommandMethod.DELETE, uri)
        command.id = id if id else str(uuid4())

        if self.to:
            command.to = self.to

        return command

    async def process_command_async(
        self,
        command: Command
    ) -> Command:
        """Process a command async.

        Args:
            command (Command): the Command to process

        Returns:
            Command: the response
        """
        command.id = command.id if command.id else str(uuid4())
        return await self.client.process_command_async(command)

    def build_resource_query(
        self,
        uri: str,
        query: Dict[str, str]
    ) -> str:
        """Build the resource query.

        Usage:

        ```py
        build_resource_query('https://take.net', { 'foo': 'bar' })
        # output: 'https://take.net?foo=bar'
        build_uri('https://take.net?', { 'foo': 'bar', 'zoo': 'buu' })
        # output: 'https://take.net?foo=bar&zoo=buu'
        ```

        Args:
            uri (str): base uri
            query (Dict[str, str]): items to add

        Returns:
            str: final uri
        """
        fixed_query = query.copy()
        for name, value in query.items():
            if value is None:
                del fixed_query[name]

        if len(fixed_query) and not uri.endswith('?'):
            uri += '?'  # noqa: WPS336

        encoded_part = urlencode(fixed_query, quote_via=RequestUtilities.quote)

        return f'{uri}{encoded_part}'

    def build_uri(self, uri: str, *args: dict) -> str:
        """Build a uri with parameters.

        Usage:

        ```py
        build_uri('https://take.net/{1}', 'foo')
        # output: 'https://take.net/foo'
        build_uri('https://take.net/{1}/{2}/{3}', 'foo', 'bar', 'zoo')
        # output: 'https://take.net/foo/bar/zoo'
        ```

        Args:
            uri (str): the template uri with {index}
            args: the parameters to replace

        Returns:
            str: the final uri
        """
        for index, value in enumerate(args):
            uri = uri.replace(f'{{{index}}}', RequestUtilities.quote(value))
        return uri
