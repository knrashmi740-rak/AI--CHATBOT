from tavily import TavilyClient

client = TavilyClient(api_key="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")

response = client.search("Who won the 2026 FIFA World Cup?")

print(response)