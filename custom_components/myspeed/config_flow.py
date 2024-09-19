"""Adds config flow for MySpeed integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    MySpeedApiClient,
    MySpeedApiClientAuthenticationError,
    MySpeedApiClientCommunicationError,
    MySpeedApiClientError,
)
from .const import CONF_API_KEY, CONF_HOSTNAME, CONF_PORT, CONF_USE_HTTP, DOMAIN, LOGGER


class MySpeedFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for MySpeed integration."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    hostname=user_input[CONF_HOSTNAME],
                    port=user_input[CONF_PORT],
                    api_key=user_input[CONF_API_KEY],
                    use_http=user_input[CONF_USE_HTTP],
                )
            except MySpeedApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except MySpeedApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except MySpeedApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_HOSTNAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOSTNAME,
                        default=(user_input or {}).get(CONF_HOSTNAME, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Optional(CONF_PORT, default=5216): int,
                    vol.Required(CONF_API_KEY): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                    vol.Optional(
                        CONF_USE_HTTP, default=False
                    ): selector.BooleanSelector(),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(
        self, hostname: str, port: int, api_key: str, *, use_http: bool
    ) -> None:
        """Validate credentials."""
        client = MySpeedApiClient(
            hostname=hostname,
            port=port,
            api_key=api_key,
            session=async_create_clientsession(self.hass),
            use_http=use_http,
        )
        await client.async_get_version()
