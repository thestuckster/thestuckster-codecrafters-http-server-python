from app.request import Request
from app.response import Response


def handle_user_agent_request(request: Request, client):

    agent = request.headers.get('User-Agent')
    headers = {
        "Content-Type": "text/plain",
        "Content-Length": str(len(agent))
    }

    response = Response(request.http_version, 200, "OK", headers, agent)
    client.sendall(response.to_response_bytes())