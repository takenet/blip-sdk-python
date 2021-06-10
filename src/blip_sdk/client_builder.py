from typing import Callable

from lime_python import (ExternalAuthentication, KeyAuthentication,
                         PlainAuthentication, Transport)

from .application import Application
from .client import Client


class ClientBuilder:
    """Builder class to generate a SDK client."""

    def __init__(self) -> None:
        self.__application = Application()
        self.__transport_factory: Callable[[], Transport] = None

    def with_application(self, application: Application):
        self.__application = application
        return self

    def with_identifier(self, identifier: str):
        self.__application.identifier = identifier
        return self

    def with_instance(self, instance: str):
        self.__application.instance = instance
        return self

    def with_domain(self, domain: str):
        self.__application.domain = domain
        return self

    def with_scheme(self, scheme: str):
        self.__application.scheme = scheme
        return self

    def with_hostname(self, hostname: str):
        self.__application.hostname = hostname
        return self

    def with_port(self, port: int):
        self.__application.port = port
        return self

    def with_access_key(self, access_key: str):
        self.__application.authentication = KeyAuthentication(access_key)
        return self

    def with_password(self, password: str):
        self.__application.authentication = PlainAuthentication(password)
        return self

    def with_token(self, token: str, issuer: str = None):
        self.__application.authentication = ExternalAuthentication(
            token,
            issuer
        )
        return self

    def with_issuer(self, issuer: str):
        if isinstance(self.__application.authentication, ExternalAuthentication):  # noqa: E501
            self.__application.authentication.issuer = issuer
        else:
            self.__application.authentication = ExternalAuthentication(
                None, issuer
            )
        return self

    def with_compression(self, compression: str):
        self.__application.compression = compression
        return self

    def with_encryption(self, encryption: str):
        self.__application.encryption = encryption
        return self

    def with_routing_rule(self, routing_rule: str):
        self.__application.presence['routingRule'] = routing_rule
        return self

    def with_echo(self, echo: str):
        self.__application.presence['echo'] = echo
        return self

    def with_priority(self, priority: str):
        self.__application.presence['priority'] = priority
        return self

    def with_round_robin(self, round_robin: str):
        self.__application.presence['roundRobin'] = round_robin
        return self

    def with_notify_consumed(self, notify_consumed: bool):
        self.__application.notify_consumed = notify_consumed
        return self

    def with_transport_factory(
        self,
        transport_factory: Callable[[], Transport]
    ):
        self.__transport_factory = transport_factory
        return self

    def with_command_timeout(self, command_timeout: int):
        self.__application.command_timeout = command_timeout
        return self

    def build(self) -> Client:
        if self.__transport_factory is None:
            raise ValueError(
                'You must pass a Transport Factory using with_transport_factory before call build'  # noqa: E501
            )
        uri = f'{self.__application.scheme}://{self.__application.hostname}:{self.__application.port}'  # noqa: E501, WPS221
        return Client(uri, self.__transport_factory, self.__application)
