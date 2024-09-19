"""MySpeed API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class MySpeedApiClientError(Exception):
    """Exception to indicate a general API error."""


class MySpeedApiClientCommunicationError(
    MySpeedApiClientError,
):
    """Exception to indicate a communication error."""


class MySpeedApiClientAuthenticationError(
    MySpeedApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise MySpeedApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class MySpeedApiClient:
    """MySpeed API Client."""

    def __init__(
        self,
        hostname: str,
        port: int,
        api_key: str,
        session: aiohttp.ClientSession,
        *,
        use_http: bool = False,
    ) -> None:
        """MySpeed API Client."""
        self._hostname = hostname
        self._port = port
        self._api_key = api_key
        self._session = session
        self._base_url = f"{'http' if use_http else 'https'}://{hostname}:{port}/api"

    def _get_url(self, endpoint: str) -> str:
        """
        Get the full URL for the API endpoint.

        Args:
            endpoint (str): The endpoint to get the URL for.

        Returns:
            str: The full URL to the API endpoint.

        """
        return self._base_url + "/" + endpoint.lstrip("/")

    async def async_get_version(self) -> Any:
        """Get the server version."""
        return await self._api_wrapper(method="get", endpoint="info/version")

    async def async_get_servers(self, provider: str) -> Any:
        """Get the available server for the provider."""
        return await self._api_wrapper(method="get", endpoint=f"info/server/{provider}")

    async def async_get_interface(self) -> Any:
        """Get the available interface to use for the speedtest."""
        return await self._api_wrapper(method="get", endpoint="info/interfaces")

    async def async_get_speedtest_statistics(self, days: int = 1) -> Any:
        """Get the speedtest statistics for given days."""
        return await self._api_wrapper(
            method="get", endpoint="speedtests/statistics", params={"days": days}
        )

    async def async_get_speedtest_averages(self, days: int = 7) -> Any:
        """Get the average speedtest results for given days."""
        return await self._api_wrapper(
            method="get", endpoint="speedtests/averages", params={"days": days}
        )

    async def async_get_speedtest(self, speedtest_id: int) -> Any:
        """Get a single speedtest by it's id."""
        return await self._api_wrapper(
            method="get", endpoint=f"speedtests/{speedtest_id}"
        )

    async def async_list_speedtests(
        self,
        hours: int | None = None,
        start: int | None = None,
        limit: int | None = None,
    ) -> Any:
        """Get a list of speedtests."""
        return await self._api_wrapper(
            method="get",
            endpoint="speedtests",
            params={"hours": hours, "start": start, "limit": limit},
        )

    async def async_run_speedtest(self) -> Any:
        """Run a single speedtest."""
        return await self._api_wrapper(method="post", endpoint="speedtests/run")

    async def async_pause_speedtest(self, resume_h: int = -1) -> Any:
        """Pause the automated speedtests."""
        return await self._api_wrapper(
            method="post", endpoint="speedtests/pause", data={"resumeIn": resume_h}
        )

    async def async_continue_speedtest(self) -> Any:
        """Resume with the automated speedtests."""
        return await self._api_wrapper(method="post", endpoint="speedtests/continue")

    async def async_delete_speedtest(self, speedtest_id: int) -> Any:
        """Delete a single speedtest."""
        return await self._api_wrapper(
            method="delete", endpoint=f"speedtests/{speedtest_id}"
        )

    async def async_get_config(self) -> Any:
        """Get the MySpeed configuration."""
        return await self._api_wrapper(method="get", endpoint="config")

    async def async_set_config_key(self, key: str, value: Any) -> Any:
        """Set a new value for a configuration key."""
        return await self._api_wrapper(
            method="patch", endpoint=f"config/{key}", data={"value": value}
        )

    async def async_get_speedtest_status(self) -> Any:
        """Get speedtest status."""
        return await self._api_wrapper(method="get", endpoint="speedtests/status")

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        speedtest_status = await self.async_get_speedtest_status()
        averages = await self.async_get_speedtest_averages()
        statistics = await self.async_get_speedtest_statistics()

        return {
            "status": speedtest_status,
            "averages": averages[1:],
            "last_test": averages[0],
            "statistics": {
                "tests": statistics.get("tests"),
                "ping": statistics.get("ping"),
                "download": statistics.get("download"),
                "upload": statistics.get("upload"),
                "time": statistics.get("time"),
            },
        }

    async def _api_wrapper(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        headers = headers or {}
        headers["password"] = self._api_key
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=self._get_url(endpoint),
                    headers=headers,
                    json=data,
                    params=params,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise MySpeedApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise MySpeedApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise MySpeedApiClientError(
                msg,
            ) from exception
