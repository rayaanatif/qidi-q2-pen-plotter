#!/usr/bin/env python3
"""Q2 Pen Plotter - local app.
Serves the plotter page on this computer only (127.0.0.1) and passes uploads/commands to the printer's Moonraker API.
Needs only Python 3.8+ (no extra packages). Run:  python3 q2_plotter.py   (Windows: py q2_plotter.py)
"""
import json, os, re, secrets, socket, sys, threading, time, uuid, webbrowser
import urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = secrets.token_urlsafe(24)
PORT = int(os.environ.get("Q2_PORT", "8765"))
PHONE_PORT = int(os.environ.get("Q2_PHONE_PORT", "8766"))
PHONE_TOKEN = secrets.token_urlsafe(9)
PHOTO = {"data": None, "ts": 0.0}
PHONE_SRV = {"srv": None}
MAX_PHOTO = 20 * 1024 * 1024
HOST_RE = re.compile(r"^[A-Za-z0-9.\-]+(:\d{1,5})?$")
NAME_RE = re.compile(r"[^\w.\-]")

def page():
    with open(os.path.join(HERE, "page.html"), "r", encoding="utf-8") as f:
        return f.read().replace("__TOKEN__", TOKEN).encode("utf-8")

def bases(ip):
    """try the address as given, then Moonraker's own port"""
    if not HOST_RE.match(ip or ""):
        raise ValueError("bad printer address")
    out = ["http://" + ip]
    if ":" not in ip:
        out.append("http://" + ip + ":7125")
    return out

def call(ip, path, data=None, headers=None, timeout=20, method=None):
    last = None
    for b in bases(ip):
        req = urllib.request.Request(b + path, data=data, headers=headers or {}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                try:
                    return json.loads(body.decode("utf-8") or "{}")
                except ValueError:
                    return {}
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            try:
                msg = json.loads(msg).get("error", {}).get("message", msg)
            except Exception:
                pass
            raise RuntimeError("printer said %s: %s" % (e.code, msg))
        except Exception as e:
            last = e
    raise RuntimeError("cannot reach printer (%s)" % last)

def upload(ip, name, gcode, start):
    boundary = "----q2plot" + uuid.uuid4().hex
    parts = []
    def field(k, v):
        parts.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (boundary, k, v)).encode())
    field("root", "gcodes")
    if start:
        field("print", "true")
    parts.append(("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"%s\"\r\nContent-Type: application/octet-stream\r\n\r\n" % (boundary, name)).encode())
    parts.append(gcode.encode("utf-8"))
    parts.append(("\r\n--%s--\r\n" % boundary).encode())
    call(ip, "/server/files/upload", b"".join(parts), {"Content-Type": "multipart/form-data; boundary=" + boundary}, timeout=60, method="POST")

PHONE_HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bed photo</title><style>
body{font:16px/1.45 system-ui,-apple-system,sans-serif;margin:0;padding:18px;background:#0f161c;color:#e4ebf0}
h1{font-size:20px;margin:0 0 6px}p{margin:8px 0;color:#9fb0bc}ol{padding-left:20px;color:#c5d1d9}
.btn{display:block;width:100%;box-sizing:border-box;margin:14px 0 6px;padding:16px;border:0;border-radius:8px;background:#7f9bff;color:#0b1220;font:600 18px system-ui;text-align:center}
.btn.alt{background:#24323d;color:#e4ebf0}
img{max-width:100%;border-radius:6px;margin-top:10px;display:block}
#st{margin-top:10px;font-weight:600}
input[type=file]{display:none}
</style></head><body>
<h1>Photo of the bed</h1>
<ol><li>Open the printer door or lid.</li><li>Hold the phone level, directly above the middle of the bed.</li><li>Get the whole paper sheet in frame, with all four corners visible and good light.</li></ol>
<label class="btn" for="f">Take photo</label><input id="f" type="file" accept="image/*" capture="environment">
<label class="btn alt" for="g">Choose from gallery</label><input id="g" type="file" accept="image/*">
<div id="st"></div><img id="pv" alt="" hidden>
<script>
const T=new URLSearchParams(location.search).get("t")||"";
async function handle(file){
  if(!file)return;const st=document.getElementById("st");st.textContent="Preparing ...";
  try{
    const bmp=await createImageBitmap(file,{imageOrientation:"from-image"});
    const sc=Math.min(1,2200/Math.max(bmp.width,bmp.height)),w=Math.round(bmp.width*sc),h=Math.round(bmp.height*sc);
    const c=document.createElement("canvas");c.width=w;c.height=h;c.getContext("2d").drawImage(bmp,0,0,w,h);
    const blob=await new Promise(r=>c.toBlob(r,"image/jpeg",0.88));
    const pv=document.getElementById("pv");pv.src=URL.createObjectURL(blob);pv.hidden=false;
    st.textContent="Sending ...";
    const r=await fetch("/phone/upload?t="+encodeURIComponent(T),{method:"POST",headers:{"Content-Type":"image/jpeg"},body:blob});
    st.textContent=r.ok?"Sent. Check the computer. You can take another.":"Upload failed ("+r.status+")";
  }catch(e){st.textContent="Failed: "+e.message}
}
document.getElementById("f").addEventListener("change",e=>handle(e.target.files[0]));
document.getElementById("g").addEventListener("change",e=>handle(e.target.files[0]));
</script></body></html>"""

def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))   # no packet is sent; just picks the outgoing interface
        ip = s.getsockname()[0]; s.close(); return ip
    except Exception:
        return "127.0.0.1"

GCODE_OK = [
    r"^PLOT_MESH( [A-Z_]+=-?\d+(\.\d+)?)*$",
    r"^(PLOT_PARK|PLOT_END|PEN_TOUCH)$",
    r"^G28( [XYZ])*$",
    r"^(M84|FIRMWARE_RESTART|RESTART)$",
]

class P(BaseHTTPRequestHandler):
    """LAN-facing handler: only the phone page and the photo upload, both need the phone token."""
    def log_message(self, *a): pass
    def _tok_ok(self):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        return q.get("t", [""])[0] == PHONE_TOKEN
    def _send(self, code, body, ctype="text/plain"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path.split("?")[0] == "/phone" and self._tok_ok():
            return self._send(200, PHONE_HTML.encode("utf-8"), "text/html; charset=utf-8")
        self._send(403, b"forbidden")
    def do_POST(self):
        if self.path.split("?")[0] != "/phone/upload" or not self._tok_ok():
            return self._send(403, b"forbidden")
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_PHOTO:
            return self._send(413, b"bad size")
        data = self.rfile.read(n)
        if data[:2] != b"\xff\xd8":
            return self._send(415, b"jpeg only")
        PHOTO["data"] = data; PHOTO["ts"] = time.time()
        self._send(200, b"ok")

def start_phone_server():
    if PHONE_SRV["srv"] is None:
        srv = ThreadingHTTPServer(("0.0.0.0", PHONE_PORT), P)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        PHONE_SRV["srv"] = srv
    return "http://%s:%d/phone?t=%s" % (lan_ip(), PHONE_PORT, PHONE_TOKEN)

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(body)
    def _json(self, code, obj): self._send(code, json.dumps(obj).encode())
    def do_GET(self):
        if self.client_address[0] not in ("127.0.0.1", "::1"):
            return self._send(403, b"forbidden", "text/plain")
        if self.path.split("?")[0] in ("/", "/index.html"):
            self._send(200, page(), "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")
    def do_POST(self):
        host = (self.headers.get("Host") or "").split(":")[0]
        if self.client_address[0] not in ("127.0.0.1", "::1") or host not in ("127.0.0.1", "localhost") or self.headers.get("X-Token") != TOKEN:
            return self._json(403, {"ok": False, "error": "forbidden"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            d = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            ip = d.get("ip", "")
            p = self.path
            if p == "/api/upload":
                name = NAME_RE.sub("_", d.get("name") or "plot.gcode") or "plot.gcode"
                g = d.get("gcode") or ""
                if not g.strip(): raise ValueError("empty G-code")
                upload(ip, name, g, bool(d.get("start")))
                return self._json(200, {"ok": True, "name": name, "lines": g.count("\n")})
            if p == "/api/gcode":
                script = (d.get("script") or "").strip()
                if not any(re.match(x, script) for x in GCODE_OK):
                    raise ValueError("this command is not allowed from the app (allowed: PLOT_*/PEN_TOUCH macros, G28, M84, restarts)")
                call(ip, "/printer/gcode/script", json.dumps({"script": script}).encode(), {"Content-Type": "application/json"}, timeout=1800, method="POST")
                return self._json(200, {"ok": True})
            if p == "/api/status":
                j = call(ip, "/printer/objects/query?print_stats&toolhead&bed_mesh", timeout=10)
                return self._json(200, {"ok": True, "status": j.get("result", {}).get("status", {})})
            if p == "/api/phone/enable":
                return self._json(200, {"ok": True, "url": start_phone_server()})
            if p == "/api/phone/latest":
                return self._json(200, {"ok": True, "ts": PHOTO["ts"], "size": len(PHOTO["data"] or b"")})
            if p == "/api/phone/photo":
                if not PHOTO["data"]:
                    return self._json(404, {"ok": False, "error": "no photo yet"})
                return self._send(200, PHOTO["data"], "image/jpeg")
            if p == "/api/cancel":
                call(ip, "/printer/print/cancel", b"{}", {"Content-Type": "application/json"}, method="POST"); return self._json(200, {"ok": True})
            if p == "/api/estop":
                call(ip, "/printer/emergency_stop", b"{}", {"Content-Type": "application/json"}, method="POST"); return self._json(200, {"ok": True})
            self._json(404, {"ok": False, "error": "unknown route"})
        except Exception as e:
            self._json(200 if False else 502, {"ok": False, "error": str(e)})

def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = "http://127.0.0.1:%d/" % PORT
    print("Q2 Pen Plotter running at", url)
    print("Close this window (or press Ctrl+C) to stop.")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
