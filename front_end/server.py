#!/usr/bin/env python3
"""
Simple HTTP server to serve the RAG Studio frontend.
Run this alongside your FastAPI backend (api_extended.py).

Usage:
    python server.py [port]
    
Default port: 3000
"""

import sys
import http.server
import socketserver
from pathlib import Path

# Get port from command line or use default
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

# Set the directory containing the HTML file
WEB_DIR = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"╔══════════════════════════════════════════════╗")
        print(f"║        RAG Studio Frontend Server           ║")
        print(f"╚══════════════════════════════════════════════╝")
        print(f"")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"📄 Serving from: {WEB_DIR}")
        print(f"")
        print(f"Open your browser and navigate to:")
        print(f"  → http://localhost:{PORT}/rag_studio.html")
        print(f"")
        print(f"Make sure your FastAPI backend is running at:")
        print(f"  → http://localhost:8000")
        print(f"")
        print(f"Press Ctrl+C to stop the server")
        print(f"")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n\n👋 Server stopped")
            sys.exit(0)
