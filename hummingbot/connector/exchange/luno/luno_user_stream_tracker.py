#!/usr/bin/env python

import asyncio
import logging
from typing import (
    Optional
)
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.logger import HummingbotLogger
from hummingbot.core.data_type.user_stream_tracker import UserStreamTracker
from hummingbot.core.utils.async_utils import (
    safe_ensure_future,
    safe_gather,
)
from hummingbot.connector.exchange.luno.luno_api_user_stream_data_source import LunoAPIUserStreamDataSource
from hummingbot.connector.exchange.luno.luno_auth import LunoAuth


class LunoUserStreamTracker(UserStreamTracker):
    _lust_logger: Optional[HummingbotLogger] = None

    @classmethod
    def logger(cls) -> HummingbotLogger:
        if cls._lust_logger is None:
            cls._lust_logger = logging.getLogger(__name__)
        return cls._lust_logger

    def __init__(self,
                 kraken_auth: LunoAuth):
        super().__init__()
        self._ev_loop: asyncio.events.AbstractEventLoop = asyncio.get_event_loop()
        self._data_source: Optional[UserStreamTrackerDataSource] = None
        self._user_stream_tracking_task: Optional[asyncio.Task] = None
        self._kraken_auth: LunoAuth = kraken_auth

    @property
    def data_source(self) -> UserStreamTrackerDataSource:
        if not self._data_source:
            self._data_source = LunoAPIUserStreamDataSource(kraken_auth=self._kraken_auth)
        return self._data_source

    @property
    def exchange_name(self) -> str:
        return "luno"

    async def start(self):
        self._user_stream_tracking_task = safe_ensure_future(
            self.data_source.listen_for_user_stream(self._ev_loop, self._user_stream)
        )
        await safe_gather(self._user_stream_tracking_task)
