import logging

from dependency_injector import containers, providers

from portal_api import storages, config, services


class Container(containers.DeclarativeContainer):
    logger = logging.getLogger(__name__)

    data_loader = providers.ThreadSafeSingleton(storages.DataLoaderWeb, logger=logger, data_url=config.data_url())

    storage = providers.Factory(storages.MemoryStorage, data_loader=data_loader)
    zap_portal = providers.Factory(services.Portal, storage=storage, restrictions=services.ZapRestrictions())
    viva_real_portal = providers.Factory(services.Portal, storage=storage, restrictions=services.VivaRealRestrictions())
