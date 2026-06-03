from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')

    def log_message(self, format, *args):
        pass  

def run_health_server(port=8080):
    """Запускает HTTP сервер для health checks"""
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f'Health check server running on port {port}')
    server.serve_forever()

def start_health_server_background():
    """Запускает HTTP сервер в фоновом потоке"""
    thread = threading.Thread(target=run_health_server, daemon=True)
    thread.start()
