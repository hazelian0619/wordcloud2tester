from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {
            "status": "success",
            "message": "API is working",
            "method": "GET"
        }
        import json
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {
            "status": "success",
            "message": "API is working",
            "method": "POST"
        }
        import json
        self.wfile.write(json.dumps(response).encode('utf-8'))
