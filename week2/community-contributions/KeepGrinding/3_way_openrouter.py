import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(base_url="https://openrouter.ai/api/v1/", api_key=os.getenv('OPENROUTER_API_KEY'))

# Consolidate bots into a structured list
bots = [
    {"name": "Alex", "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "system": "You are a chatbot who is very argumentative; you disagree with anything in the conversation and you challenge everything, in a snarky way."},
    {"name": "Blake", "model": "openai/gpt-oss-120b:free", "system": "You are a very polite, courteous chatbot. You try to agree with everything the other person says, or find common ground."},
    {"name": "Casey", "model": "z-ai/glm-4.5-air:free", "system": "You are a helpful assistant. You provide accurate and concise information."}
]

conversation = [("Alex", "Hi there"), ("Blake", "Hi"), ("Casey", "Hello")]

def get_reply(bot):
    convo_text = "".join([f"{spk}: {msg}\n" for spk, msg in conversation])
    others = ", ".join([b["name"] for b in bots if b["name"] != bot["name"]])
    
    response = client.chat.completions.create(
        model=bot["model"],
        messages=[
            {"role": "system", "content": bot["system"]},
            {"role": "user", "content": f"You are {bot['name']}, in conversation with {others}. The conversation so far:\n{convo_text}Respond with what you say next as {bot['name']}."}
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("--- Initial Conversation ---")
    for speaker, msg in conversation:
        print(f"\n[{speaker}]: {msg}")
        
    print("\n--- LLM Generated Turns ---")
    for bot in bots:
        reply = get_reply(bot)
        print(f"\n[{bot['name']}]: {reply}")
        conversation.append((bot['name'], reply))
