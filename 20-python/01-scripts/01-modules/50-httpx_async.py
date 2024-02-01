import asyncio
import httpx
from typing import Any, Protocol

base_url = 'https://kubernetes.io'
# max_ka_conn <= max_conn
limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
client = httpx.AsyncClient(base_url=base_url, timeout=10, limits=limits)


class OutputHandler(Protocol):
    def __call__(self, url: str, text: str | None, e: Exception | None = None) -> Any: ...


async def fetch_doc(url: str) -> str:
    r = await client.get(url)
    assert r.status_code == 200, f'status_code expected 200, but got {r.status_code}'
    return r.text


async def batch_fetch(urls: list[dict[str, str]], output_handle: OutputHandler) -> list[Any]:
    async def _fetch(url):
        try:
            text = await fetch_doc(url)
            return output_handle(url, text)
        except Exception as e:
            return output_handle(url, None, e)

    return await asyncio.gather(*(_fetch(url['url']) for url in urls))


def save2list(url: str, text: str | None, e: Exception | None = None) -> dict[str, str]:
    if e:
        print(f'fetch error, {url=}, {e=}')
    return {'url': url, 'text': text}


doc_urls = [
    {'url': '/zh-cn/docs/home/', 'name': '主页'},
    {'url': '/zh-cn/docs/home/supported-doc-versions/', 'name': 'Kubernetes 文档支持的版本'},
    {'url': '/zh-cn/docs/setup/', 'name': '入门'},
    {'url': '/zh-cn/docs/setup/learning-environment/', 'name': '学习环境'},
    {'url': '/zh-cn/docs/setup/production-environment/', 'name': '生产环境'},
    {'url': '/zh-cn/docs/concepts/overview/working-with-objects/names/', 'name': '对象名称和 ID'},
    {'url': '/zh-cn/docs/concepts/overview/working-with-objects/labels/', 'name': '标签和选择算符'},
    {'url': '/zh-cn/docs/concepts/overview/working-with-objects/namespaces/', 'name': '名字空间'},
    {'url': '/zh-cn/docs/concepts/overview/working-with-objects/annotations/', 'name': '注解'},
]

docs = asyncio.run(batch_fetch(doc_urls, save2list))
print({d['url']: d['text'] is not None for d in docs})
