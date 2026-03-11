from core.instrumentation import instrument_tool

def search_product(product):
    return f"Found {product} for $1200"

def main():

    tool = instrument_tool(
        agent_name="shopping_agent",
        tool_name="search_product",
        func=search_product
    )

    result = tool("laptop")

    print("Tool result:", result)

if __name__ == "__main__":
    main()
