from js import Response, Headers, fetch, Request
from urllib.parse import urlparse

async def on_fetch(request, env, ctx):
    URL = urlparse(request.url)
    response = await env.Assets.fetch(request)

    if response.status == 404:
        path = URL.path
        src_url = f'{URL.scheme}://{URL.netloc}/src{path}'
        response = await env.Assets.fetch(src_url)
        #ParseResult(scheme='https', netloc='192.168.0.111', path='/main.py', params='', query='', fragment='')

    content_type = response.headers.get("content-type")
    headers = Headers.new()
    headers.append("content-type", content_type)
    #headers.append("Cross-Origin-Opener-Policy", 'same-origin')
    #headers.append("Cross-Origin-Embedder-Policy", 'require-corp')


    return Response.new(response.body, headers=headers, status=response.status)