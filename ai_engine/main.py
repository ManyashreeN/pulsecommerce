from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from intent import detect_intent
from response import generate_response
from recommend import recommend_products
from context import ConversationContext

app = FastAPI(title="AI Messaging Engine")

# -----------------------------
# In-memory context store (hackathon use)
# -----------------------------
user_context_store: Dict[str, ConversationContext] = {}

# -----------------------------
# Request Schema
# -----------------------------
class UserRequest(BaseModel):
    user_id: str
    message: str
    context: Dict[str, Any] = {}


# -----------------------------
# Helper: Get/Create Context
# -----------------------------
def get_user_context(user_id: str) -> ConversationContext:
    if user_id not in user_context_store:
        user_context_store[user_id] = ConversationContext()
    return user_context_store[user_id]


# -----------------------------
# MAIN API: Generate Response
# -----------------------------
@app.post("/generate-response")
def generate_response_api(req: UserRequest):

    # 1️⃣ Get user context
    context = get_user_context(req.user_id)

    # 2️⃣ Detect intent + entities
    intent, entities = detect_intent(req.message)

    # 3️⃣ Update context
    context.update_history(req.message, intent)

    # 4️⃣ Get recommendations (if needed)
    product_suggestions = recommend_products(intent, entities)

    # 5️⃣ Generate response
    reply = generate_response(
        intent=intent,
        entities=entities,
        context=context,
        products=product_suggestions
    )

    # 6️⃣ Return response
    return {
        "reply": reply,
        "intent": intent,
        "products": product_suggestions
    }


# -----------------------------
# OPTIONAL: Recommendation API
# -----------------------------
@app.post("/recommend-products")
def recommend_products_api(req: UserRequest):

    intent, entities = detect_intent(req.message)
    products = recommend_products(intent, entities)

    return {
        "products": products
    }


# -----------------------------
# Health Check (for testing)
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI Engine is running 🚀"}