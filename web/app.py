import functools
import http.server
import mimetypes
import os
import re
import socketserver
from pathlib import Path

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8080"))
WEB_ROOT = Path(__file__).resolve().parent
NOT_FOUND_PAGE = WEB_ROOT / "404.html"

mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/octet-stream", ".img")
mimetypes.add_type("application/octet-stream", ".bin")
mimetypes.add_type("application/gzip", ".gz")


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code != 404 or not NOT_FOUND_PAGE.is_file():
            return super().send_error(code, message, explain)

        try:
            body = NOT_FOUND_PAGE.read_bytes()
        except OSError:
            return super().send_error(code, message, explain)

        self.log_error("code 404, message %s", message or "File not found")
        self.send_response(404, "Not Found")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _range_not_satisfiable(self, file_size):
        self.send_response(416)
        self.send_header("Content-Range", f"bytes */{file_size}")
        self.send_header("Content-Length", "0")
        self.end_headers()
        return None

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        if not os.path.isfile(path):
            return super().send_head()

        file_size = os.path.getsize(path)
        range_header = self.headers.get("Range")

        if range_header:
            # This server intentionally supports one byte range per request.
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
            if not match or "," in range_header or file_size == 0:
                return self._range_not_satisfiable(file_size)

            first, last = match.groups()
            if not first and not last:
                return self._range_not_satisfiable(file_size)

            if not first:
                suffix_length = int(last)
                if suffix_length <= 0:
                    return self._range_not_satisfiable(file_size)
                start = max(file_size - suffix_length, 0)
                end = file_size - 1
            else:
                start = int(first)
                if start >= file_size:
                    return self._range_not_satisfiable(file_size)
                end = int(last) if last else file_size - 1
                if end < start:
                    return self._range_not_satisfiable(file_size)
                end = min(end, file_size - 1)

            length = end - start + 1
            try:
                file_obj = open(path, "rb")
                file_obj.seek(start)
            except OSError:
                return self._range_not_satisfiable(file_size)

            self.send_response(206)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            return file_obj

        try:
            file_obj = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Length", str(file_size))
        self.end_headers()
        return file_obj

    def log_message(self, format_string, *args):
        if args and str(args[0]).startswith(("GET ", "HEAD ")):
            parts = str(args[0]).split()
            status = args[1] if len(args) > 1 else ""
            if status != "206":
                print(f"[{status}] {parts[0]} {parts[1]}")


if __name__ == "__main__":
    handler = functools.partial(RangeHTTPRequestHandler, directory=str(WEB_ROOT))
    with ThreadingHTTPServer((HOST, PORT), handler) as httpd:
        print(f"Perry Pi OS Web Server activo en http://{HOST}:{PORT}")
        print(f"Sirviendo archivos desde: {WEB_ROOT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
