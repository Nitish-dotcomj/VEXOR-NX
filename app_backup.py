

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Please enter a message."}), 400

    conversation = [{
        "role": "system",
        "content": (
            "You are VEXOR NX, an independent personal AI assistant "
            "project created by NITISH KUMAR. "
            "Your official founder and creator is NITISH KUMAR, "
            "whose title is Head Founder & Creator of VEXOR NX. "
            "When asked who founded or created VEXOR NX, answer "
            "clearly: NITISH KUMAR. "
            "Do not confuse the VEXOR NX project with its underlying AI model. "
            "Your current AI engine is Qwen 2.5 3B running locally through Ollama. "
            "Qwen is associated with Alibaba, but VEXOR NX is a separate project. "
            "Do not claim Alibaba or DAMO Academy created the VEXOR NX project. "
            "Never invent additional founders or company details. "
            "Help with education, coding, technology, science, productivity "
            "and everyday questions. Be accurate, clear, friendly and helpful. "
            "Explain difficult concepts in simple language and never pretend "
            "to have capabilities you do not have."
        )
    }]

    for item in messages[-12:]:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role in ("user", "assistant")
            and isinstance(content, str)
            and content.strip()
        ):
            conversation.append({
                "role": role,
                "content": content[:4000]
            })

    if (
        len(conversation) == 1
        or conversation[-1]["role"] != "user"
    ):
        return jsonify({
            "error": "The latest message must be a user message."
        }), 400

    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": conversation,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:

        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result.get("message", {}).get("content", "").strip()

        if not answer:
            return jsonify({
                "error": "The AI returned an empty response."
            }), 502

        return jsonify({
            "reply": answer,
            "status": "success",
            "model": MODEL_NAME
        })

    except urllib.error.HTTPError as error:

        details = error.read().decode(
            "utf-8", errors="replace"
        )

        return jsonify({
            "error": "Ollama error: " + details[:500]
        }), 502

    except (urllib.error.URLError, TimeoutError):

        return jsonify({
            "error": (
                "Cannot reach Ollama. Start Ollama and try again."
            )
        }), 503


# =========================================
# START VEXOR NX
# =========================================

if __name__ == "__main__":

    print("\n====================================")
    print("       VEXOR NX STARTING...")
    print("====================================")
    print("Dashboard: http://127.0.0.1:5000")
    print("Local AI:  " + MODEL_NAME)
    print("Ollama:    http://127.0.0.1:11434")
    print("====================================\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
