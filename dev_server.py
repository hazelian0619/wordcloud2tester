#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地开发服务器：模拟 Vercel 的路由行为
  - GET  /                -> frontend/index.html
  - GET  /<file>          -> frontend/<file> (静态资源)
  - POST /api/path-expand -> api/path-expand.py 里的 handler
运行前会加载 .env。
"""
import os
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---- 加载 .env ----
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    print("✅ 已加载 .env")
except Exception as e:
    print(f"⚠️  未能加载 .env: {e}")

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(ROOT, "frontend")

# ---- 动态导入 api/path-expand.py（文件名含连字符，不能直接 import）----
_spec = importlib.util.spec_from_file_location(
    "path_expand", os.path.join(ROOT, "api", "path-expand.py")
)
path_expand = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(path_expand)
ApiHandler = path_expand.handler  # Vercel 风格的 BaseHTTPRequestHandler 子类

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
}


class DevHandler(BaseHTTPRequestHandler):
    def _serve_static(self, path):
        if path == "/" or path == "":
            path = "/index.html"
        # 防目录穿越
        safe = os.path.normpath(path).lstrip("/")
        full = os.path.join(FRONTEND, safe)
        if not full.startswith(FRONTEND) or not os.path.isfile(full):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        ext = os.path.splitext(full)[1]
        with open(full, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(ext, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _delegate_to_api(self, method):
        """把请求交给 api handler 处理，复用它的 rfile/wfile/headers。"""
        api = ApiHandler.__new__(ApiHandler)
        api.rfile = self.rfile
        api.wfile = self.wfile
        api.headers = self.headers
        api.request_version = self.request_version
        api.command = method
        api.path = self.path
        api.send_response = self.send_response
        api.send_header = self.send_header
        api.end_headers = self.end_headers
        getattr(api, f"do_{method}")()

    def do_GET(self):
        if self.path.startswith("/api/path-expand"):
            self._delegate_to_api("GET")
        else:
            self._serve_static(self.path)

    def do_POST(self):
        if self.path.startswith("/api/path-expand"):
            self._delegate_to_api("POST")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        if self.path.startswith("/api/path-expand"):
            self._delegate_to_api("OPTIONS")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(f"[dev] {self.address_string()} {fmt % args}")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"🚀 本地服务器启动: http://localhost:{port}")
    print(f"   模型: {os.getenv('OPENAI_MODEL')}  |  base: {os.getenv('OPENAI_BASE_URL')}")
    ThreadingHTTPServer(("0.0.0.0", port), DevHandler).serve_forever()
