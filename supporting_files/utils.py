import httpx

class utils_pt:

    async def api_methods(self, method, urls, payload, headers):
        async with httpx.AsyncClient() as client:
            if method == "POST":
                if payload is None:
                    raise ValueError("POST request requires payload")
                response = await client.post(urls, json= payload, headers= headers)
                return response
            elif method == "GET":
                response = await client.get(urls)
                return response
            elif method == "PUT":
                if payload is None:
                    raise ValueError("POST request requires payload")
                response = await client.put(urls, json= payload)
                return response
            elif method == "DELETE":
                response = await client.delete(urls)
                return response