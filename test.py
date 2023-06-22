from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        # Parse the URL and extract the request parameters
        url_parts = urlparse(self.path)
        query_params = parse_qs(url_parts.query)

        # Parse the request body for POST requests
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode()
        post_params = parse_qs(post_body)

        # Combine GET and POST parameters
        all_params = {**query_params, **post_params}

        # Send response headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Build the response content
        response_content = f"Request received on URL: {url_parts.path}<br><br>"
        response_content += "Request Parameters:<br>"
        for param, values in all_params.items():
            response_content += f"{param}: {', '.join(values)}<br>"

        # Send the response content
        self.wfile.write(response_content.encode())

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

# Run the server on port 8000
run_server(8080)
