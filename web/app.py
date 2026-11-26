import http.server
import socketserver
import os
import re
import mimetypes

PORT = 8080

mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/octet-stream", ".img")
mimetypes.add_type("application/octet-stream", ".bin")


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        guessed, _ = mimetypes.guess_type(path)
        if guessed:
            return guessed
        return super().guess_type(path)

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for index_name in ("index.html", "index.htm"):
                candidate = os.path.join(path, index_name)
                if os.path.isfile(candidate):
                    path = candidate
                    break

        if not os.path.isfile(path):
            return super().send_head()

        file_size = os.path.getsize(path)
        range_header = self.headers.get("Range")

        if range_header:
            match = re.match(r"bytes=(\d+)-(\d*)", range_header.strip())
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else file_size - 1

                if start >= file_size or end >= file_size or start > end:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{file_size}")
                    self.end_headers()
                    return None

                length = end - start + 1
                f = open(path, "rb")
                f.seek(start)
                self.send_response(206)
                self.send_header("Content-type", self.guess_type(path))
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self.end_headers()
                return f

        f = open(path, "rb")
        self.send_response(200)
        self.send_header("Content-type", self.guess_type(path))
        self.send_header("Content-Length", str(file_size))
        self.end_headers()
        return f

    def log_message(self, format, *args):
        if args and str(args[0]).startswith(("GET ", "HEAD ")):
            parts = str(args[0]).split()
            status = args[1] if len(args) > 1 else ""
            if status != "206":
                print(f"[{status}] {parts[0]} {parts[1]}")


if __name__ == "__main__":
    with ThreadingHTTPServer(("", PORT), RangeHTTPRequestHandler) as httpd:
        print(f"Perry Pi OS Web Server activo en http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
