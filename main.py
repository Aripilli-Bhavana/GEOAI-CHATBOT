# check.py

import requests
from configparser import ConfigParser
from src.matcher.matcher import get_relevant_metadata

# Load LLM server config
config = ConfigParser()
config.read("conf/server.conf")
LLM_HOST = config.get("llm", "host", fallback="localhost")
LLM_PORT = config.get("llm", "port", fallback="11434")
LLM_URL = f"http://{LLM_HOST}:{LLM_PORT}/api/chat"  # ✅ FIXED

print("GEO-Him")
model_choice = "mistral:latest"
print(f" Using model: {model_choice}")
print(f" LLM Server: {LLM_URL}")

while True:
    user_query = input("\nEnter your question (or 'quit' to exit): ").strip()

    if user_query.lower() in ['quit', 'exit', 'q']:
        print(" Bye!")
        break

    if not user_query:
        print(" Sorry, no data found as per your query.")
        continue

    print("🔍 Searching relevant datasets...")
    context = get_relevant_metadata(user_query)

    if not context:
        print("\n--- Response ---")
        print(" Sorry, no data found as per your query.")
        continue

    system_prompt = (
        "You are a helpful GIS assistant for Uttarakhand geographical data. "
        "IMPORTANT INSTRUCTIONS:\n"
        "1. Answer ONLY using the provided dataset context below\n"
        "2. If the question cannot be answered from the dataset, respond with: 'Sorry, no data found as per your query'\n"
        "3. Do not make assumptions or use general knowledge\n"
        "4. Be specific and reference the exact dataset/table when answering\n"
        "5. If asked about data not in the provided context, say no data is available\n"
    )

    final_prompt = f"""{system_prompt}

Context from Uttarakhand Datasets:
{context}

User Question: {user_query}

Answer (based only on the above dataset context):"""

    print("\n--- Prompt sent to LLM ---")
    print(f"Context length: {len(context)} characters")
    print(f"Query: {user_query}")

    try:
        print("\n🤖 Generating response...")
        response = requests.post(
            LLM_URL,
            json={
                "model":"mistral:latest",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{context}\n\n{user_query}"}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            },
            
        )

        if response.status_code == 200:
            result = response.json().get("message", {}).get("content", "No response from LLM.")
        else:
            result = f" Error: HTTP {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        result = " Request timed out. Please check if the LLM server is running."
    except requests.exceptions.ConnectionError:
        result = f" Cannot connect to LLM server at {LLM_URL}. Please check if Ollama is running."
    except Exception as e:
        result = f" Error contacting LLM server: {e}"

    print("\n--- LLM Response ---")
    print(result)
    