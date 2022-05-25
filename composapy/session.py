import os
from System import Uri
from CompAnalytics import IServices
from CompAnalytics.IServices import *


class SessionException(Exception):
    pass


class UriNotConfiguredError(SessionException):
    pass


class Session:
    """Holds connection and binding state for composapy api usage."""

    @property
    def app_service(self) -> IServices.IApplicationService:
        """A composable analytics csharp binding to the IServices.IApplicationService (otherwise
        known as a dataflow service) object.
        """
        return self.services["ApplicationService"]

    @property
    def table_service(self) -> IServices.ITableService:
        """A composable analytics csharp binding to the IServices.ITableService object."""
        return self.services["TableService"]

    @property
    def api_token(self) -> str:
        return self._api_token

    @property
    def uri(self) -> str:
        return str(self.connection_settings.Uri)

    def __init__(self, api_token: str, uri: str = None):
        if uri is None and os.environ.get("APPLICATION_URI") is None:
            raise UriNotConfiguredError(
                "A uri must be configured by either setting an "
                "environment variable named APPLICATION_URI, "
                "or by passing it in through the Session "
                "initialization parameters."
            )
        uri = uri if uri is not None else os.getenv("APPLICATION_URI")

        self.connection_settings = IServices.Deploy.ConnectionSettings()
        self.connection_settings.Uri = Uri(uri)
        self.connection_settings.AuthMode = IServices.Deploy.AuthMode.Api
        self.connection_settings.ApiKey = api_token
        self._api_token = api_token

        self.ResourceManager = IServices.Deploy.ResourceManager(
            self.connection_settings
        )

        self.services = {}
        for method in self.ResourceManager.AvailableServices():
            method_name = self.get_method_name(method)
            try:
                self.services[method_name] = self.ResourceManager.CreateAuthChannel[
                    method
                ](method_name)

            except:
                self.services[
                    method_name
                ] = self.ResourceManager.CreateAuthChannelNoWebScripting[method](
                    method_name
                )

    @staticmethod
    def get_method_name(method):
        return str(method).split(".")[-1][1:]
