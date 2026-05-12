from sqlmodel import select, Session
from typing import List

from .models import ProxyProvider, Proxy


def get_proxy_provider(session: Session, provider_id: int) -> ProxyProvider | None:
    return session.get(ProxyProvider, provider_id)


def get_proxy_providers(session: Session, offset: int = 0, limit: int = 100) -> List[ProxyProvider]:
    query = select(ProxyProvider).offset(offset).limit(limit)
    results = session.exec(query)
    return results.all()


def create_proxy_provider(session: Session, provider: ProxyProvider) -> ProxyProvider:
    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider


def update_proxy_provider(session: Session, provider: ProxyProvider, provider_data: ProxyProvider) -> ProxyProvider:
    update_data = provider_data.model_dump(exclude_unset=True)
    provider.sqlmodel_update(update_data)
    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider


def delete_proxy_provider(session: Session, provider: ProxyProvider) -> None:
    session.delete(provider)
    session.commit()
    return None
