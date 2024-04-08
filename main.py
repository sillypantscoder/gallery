from http.server import BaseHTTPRequestHandler, HTTPServer
import typing
import os
import pygame
import io

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
serverPort = 8072

class HttpResponse(typing.TypedDict):
	status: int
	headers: dict[str, str]
	content: bytes

def pq(path: str, q: str):
	qpath = path.split("?")[0]
	sp = qpath.split("/")[1:]
	sq = q.split("/")[1:]
	if len(sp) != len(sq): return False
	for i in range(len(sp)):
		if sq[i] == "*": continue
		if sp[i] != sq[i]: return False
	return True

def get(path: str) -> HttpResponse:
	if pq(path, "/"):
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": read_file("index.html")
		}
	if pq(path, "/index.js"):
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/javascript"
			},
			"content": read_file("index.js")
		}
	if pq(path, "/meta.json"):
		return {
			"status": 200,
			"headers": {
				"Content-Type": "application/json"
			},
			"content": read_file("meta.json")
		}
	image_filename = "pictures/" + path.split("/")[2].replace(".", "").replace("/", "") + ".png"
	if os.path.isfile(image_filename):
		if pq(path, "/image/*/"):
			return {
				"status": 200,
				"headers": {
					"Content-Type": "text/html"
				},
				"content": read_file("image.html")
			}
		if pq(path, "/image/*/thumbnail.png"):
			img = pygame.image.load(image_filename)
			maxsize = 150
			scale = 1
			size = img.get_size()
			if size[0] > size[1]:
				scale = maxsize / size[0]
			else:
				scale = maxsize / size[1]
			result = io.BytesIO()
			pygame.image.save(pygame.transform.scale(img, (size[0] * scale, size[1] * scale)), result, "thumbnail.png")
			result.seek(0)
			return {
				"status": 200,
				"headers": {
					"Content-Type": "image/png"
				},
				"content": result.read()
			}
		if pq(path, "/image/*/image.png"):
			return {
				"status": 200,
				"headers": {
					"Content-Type": "image/png"
				},
				"content": read_file(image_filename)
			}
	# 404 page
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
