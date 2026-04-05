
def detect_intent(message):
    msg = message.lower()

    entities = {}

    if "buy" in msg or "order" in msg:
        return "purchase", entities

    elif "show" in msg or "find" in msg:
        if "shoe" in msg:
            entities["category"] = "shoes"
        elif "phone" in msg:
            entities["category"] = "electronics"
        return "product_search", entities

    elif "price" in msg or "details" in msg:
        return "product_query", entities

    elif "hi" in msg or "hello" in msg:
        return "greeting", entities

    return "fallback", entities