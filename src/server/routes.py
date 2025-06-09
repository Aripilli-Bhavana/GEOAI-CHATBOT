# src/server/routes.py

from flask import Blueprint, request, jsonify
import requests
from configparser import ConfigParser
from src.matcher.matcher import get_relevant_metadata
import os

routes = Blueprint("routes", __name__)

# Load LLM configuration
def load_config():
    config = ConfigParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    config_path = os.path.join(project_root, "conf", "server.conf")
    config.read(config_path)
    
    host = config.get("llm", "host", fallback="localhost")
    port = config.get("llm", "port", fallback="11434")
    return f"http://{host}:{port}/api/generate"

LLM_URL = load_config()

@routes.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or not data.get("query", "").strip():
            return jsonify({"error": "Query is required"}), 400

        query = data["query"].strip()
        context = get_relevant_metadata(query)

        if not context:
            return jsonify({
                "response": "Sorry, no data found as per your query. I can only provide information about Uttarakhand geographical datasets.",
                "has_data": False
            })

        system_prompt = (
            "You are a GIS assistant. Follow these rules:\n"
            "1. Answer using only the dataset context.\n"
            "2. If the answer is not in context, say: 'Sorry, no data found as per your query.'\n"
            "3. Be specific and mention dataset/table names if applicable.\n"
            "4. Never make assumptions or use outside knowledge."
        )

        full_prompt = f"""{system_prompt}

Dataset Context:
{context}

User Query: {query}

Answer:"""

        payload = {
            "model": "llama3:latest",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }

        response = requests.post(LLM_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            return jsonify({
                "response": response.json().get("response", "No response from LLM."),
                "has_data": True,
                "context_length": len(context)
            })
        else:
            return jsonify({
                "error": f"LLM server error: HTTP {response.status_code}",
                "details": response.text
            }), 500

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to LLM server timed out"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Cannot connect to LLM server at {LLM_URL}"}), 503
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@routes.route("/health", methods=["GET"])
def health_check():
    try:
        test_payload = {
            "model": "llama3:latest",
            "prompt": "Test",
            "stream": False,
            "options": {"max_tokens": 1}
        }
        response = requests.post(LLM_URL, json=test_payload, timeout=5)
        llm_status = "connected" if response.status_code == 200 else "disconnected"
    except:
        llm_status = "disconnected"

    return jsonify({
        "status": "healthy",
        "llm_server": LLM_URL,
        "llm_status": llm_status
    })

@routes.route("/datasets", methods=["GET"])
def get_datasets():
    from src.matcher.matcher import load_metadata
    metadata = load_metadata()
    
    datasets = [{
        "name": name,
        "table_name": info.get("table_name"),
        "description": info.get("description"),
        "columns": list(info.get("columns", {}).keys())
    } for name, info in metadata.items()]
    
    return jsonify({"datasets": datasets})
