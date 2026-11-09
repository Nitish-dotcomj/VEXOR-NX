VEXOR NX — WEBSITE STARTER
==========================

WHAT'S INCLUDED
- / : Official futuristic public homepage
- /dashboard : Existing VEXOR NX dashboard (AI chat, voice, MediaPipe gestures, PDF reader, system monitor)
- Flask backend and API routes retained from the saved project

RUN LOCALLY (Windows PowerShell)
1. Extract this ZIP into a folder, for example C:\Users\YOURNAME\Documents\VEXOR_NX.
2. Open PowerShell in that folder.
3. Run: py -m venv .venv
4. Run: .\.venv\Scripts\Activate.ps1
5. Run: pip install -r requirements.txt
6. Start Ollama and make sure qwen2.5:3b is installed if you want local AI chat.
7. Run: python app.py
8. Open http://127.0.0.1:5000 for the official homepage.
   Open http://127.0.0.1:5000/dashboard for the AI dashboard.

PUBLIC HOSTING NOTES
- render.yaml is a starter configuration for Render. Push this folder to a GitHub repository, then create a Render Web Service from that repository.
- The free web service may sleep after inactivity; this is not guaranteed 24/7 hosting. A custom domain is optional and usually costs money.
- IMPORTANT: the current Qwen model runs through Ollama on your own computer. A hosted Render app cannot reach Ollama at 127.0.0.1 on your laptop. To make AI chat work publicly while your laptop is off, deploy a separate cloud inference service and set OLLAMA_URL to its private/reachable /api/chat endpoint and MODEL_NAME to an available model. This may have usage or hosting costs. Do not expose an unauthenticated model endpoint publicly.
- Camera access on a public site requires HTTPS; Render provides HTTPS on its hosted domain. Browser camera permission is still required.
- The PDF is selected locally in each visitor's browser; it is not uploaded to the server.

SECURITY
This is a project starter, not a hardened production deployment. Before inviting the public to use AI chat, add authentication, rate limiting, request-size limits, logging controls and a protected AI provider. Never commit API keys or passwords to GitHub.
