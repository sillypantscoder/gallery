# INIT STUFF

from http.server import BaseHTTPRequestHandler, HTTPServer
import typing

def read_file(filename: str) -> bytes:
	f = open(filename, "rb")
	t = f.read()
	f.close()
	return t

def write_file(filename: str, content: bytes):
	f = open(filename, "wb")
	f.write(content)
	f.close()

hostName = "0.0.0.0"
serverPort = 8074

class HttpResponse(typing.TypedDict):
	status: int
	headers: dict[str, str]
	content: bytes

def get(path: str) -> HttpResponse:
	print(path)
	if path == "/":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": read_file("index.html")
		}
	elif path == "/index.js":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/javascript"
			},
			"content": read_file("index.js")
		}
	elif path == "/meta.json":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "application/json"
			},
			"content": read_file("meta.json")
		}
	else: # 404 page
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": b""
		}

def post(path: str, body: bytes) -> HttpResponse:
	if False: pass
	else:
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": b""
		}

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		global running
		res = get(self.path)
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		c = res["content"]
		self.wfile.write(c)
	def do_POST(self):
		res = post(self.path, self.rfile.read(int(self.headers["Content-Length"])))
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		c = res["content"]
		self.wfile.write(c)
	def log_message(self, format: str, *args: typing.Any) -> None:
		return;
		if 400 <= int(args[1]) < 500:
			# Errored request!
			print(u"\u001b[31m", end="")
		print(args[0].split(" ")[0], "request to", args[0].split(" ")[1], "(status code:", args[1] + ")")
		print(u"\u001b[0m", end="")
		# don't output requests

if __name__ == "__main__":
	running = True
	webServer = HTTPServer((hostName, serverPort), MyServer)
	webServer.timeout = 1
	print("Server started http://%s:%s" % (hostName, serverPort))
	while running:
		try:
			webServer.handle_request()
		except KeyboardInterrupt:
			running = False
	webServer.server_close()
	print("Server stopped")