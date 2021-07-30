from lime_python import Command
from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates


class ContextsExtension(ExtensionBase):
    """Extension to handle blip media."""

    async def get_bot_contexts_async(
        self,
        skip: int = 0,
        take: int = 100,
        **kwargs
    ) -> Command:
        """Get all bot's context variables (Builder's behaviors).

        Args:
            take (int): Number of variables to be taken.
            skip (int): Number of variables to be skipped.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: It will return all users with context variables.
        """
        uri = self.build_resource_query(
            UriTemplates.CONTEXTS,
            {'$skip': skip, '$take': take, **kwargs}
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def get_context_variables(
        self,
        user_id: str,
        skip: int = 0,
        take: int = 100,
        show_value: bool = False,
        **kwargs
    ) -> Command:
        """Get all user's context variables.

        Args:
            user_id(str): User identity.
            skip (int): Number of variables to be skipped.
            take (int): Number of variables to be taken.
            show_value (bool): Says if should return variable value.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_uri(UriTemplates.USER_CONTEXT, user_id)
        uri = self.build_resource_query(
            uri,
            {
                '$skip': skip,
                '$take': take,
                'withContextValue': show_value,
                **kwargs
            }
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def get_context_variable(
        self,
        user_id: str,
        variable_name: str,
        **kwargs
    ) -> Command:
        """Get a specific user's context variable, with all information about it.

        Args:
            user_id(str): User identity.
            variable_name (str): Context variable name.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_uri(
            UriTemplates.CONTEXT_VARIABLE,
            user_id,
            variable_name
        )
        uri = self.build_resource_query(
            uri,
            {**kwargs}
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def set_context_variable(
        self,
        user_id: str,
        variable_name: str,
        variable_type: str,
        variable_value: str
    ) -> Command:
        """Get a specific user's context variable, with all information about it.

        Args:
            user_id(str): User identity.
            variable_name (str): Context variable name.
            variable_type (str): Context variable type.
            variable_value (str): Context variable value.

        Returns:
            Command
        """
        uri = self.build_uri(
            UriTemplates.CONTEXT_VARIABLE,
            user_id,
            variable_name
        )

        set_context_body = self.create_set_command(
            uri,
            type_n=variable_type,
            resource=variable_value
        )
        return await self.process_command_async(set_context_body)

    async def delete_context_variable_async(
        self,
        user_id: str,
        variable_name: str
    ) -> Command:
        """Get a specific user's context variable, with all information about it.

        Args:
            user_id(str): User identity.
            variable_name (str): Context variable name.

        Returns:
            Command
        """
        uri = self.build_uri(
            UriTemplates.CONTEXT_VARIABLE,
            user_id,
            variable_name
        )

        delete_context_body = self.create_delete_command(uri)
        return await self.process_command_async(delete_context_body)

    async def get_master_state_async(
        self,
        user_id: str,
        show_value: bool = False,
        **kwargs
    ) -> Command:
        """Get user master-state.

        Args:
            user_id(str): User identity.
            show_value (bool): Says if should return variable value.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_uri(
            UriTemplates.CONTEXT_VARIABLE,
            user_id,
            'master-state'
        )
        uri = self.build_resource_query(
            uri,
            {'withContextValue': show_value, **kwargs}
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def set_master_state(
        self,
        user_id: str,
        variable_value: str
    ) -> Command:
        """Set user master-state.

        Args:
            user_id(str): User identity.
            variable_value (str): Context variable value.

        Returns:
            Command
        """
        uri = self.build_uri(
            UriTemplates.CONTEXT_VARIABLE,
            user_id,
            'master-state'
        )

        set_context_body = self.create_set_command(
            uri,
            type_n='text/plain',
            resource=variable_value
        )
        return await self.process_command_async(set_context_body)
