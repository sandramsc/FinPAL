import asyncio

def synchronize_async_helper(fn_to_await):
    async_response = []

    async def run_and_capture_result():
        if callable(fn_to_await):
            r = await fn_to_await()
        else:
            r = await fn_to_await
        async_response.append(r)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_and_capture_result())
    loop.close()

    return async_response[0]