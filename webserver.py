#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import configparser
import datetime
import log
import threading
import time
import base64
import ssl

s_hsvr = None
s_key  = ""

FAVICON = b"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"

#----------------------------[readlog]
def readlog(logflag):
    if   logflag == 1:
        compare = "temp"
    elif logflag == 2:
        compare = "websvr"
    elif logflag == 3:
        compare = "main"
    elif logflag == 4:
        compare = "rf"
    elif logflag == 5:
        compare = "pir"
    else:
        compare = " "

    ctime = datetime.datetime.today() - datetime.timedelta(days=4)
    log = ""
    try:
        f = open("/var/log/pigc_{:s}.log".format(time.strftime("%Y-%m")),"r")
    except Exception:
        try:
            f = open("pigc_{:s}.log".format(time.strftime("%Y-%m")),"r")
        except Exception:
            return "no log found"

    while True:
        rl = f.readline()
        if not rl:
            break
        line = str(rl)
        if line.find(compare) == -1:
            continue
        try:
            date = datetime.datetime.strptime(line[:10], "%Y-%m-%d")
            if date < ctime:
                continue
        except Exception:
            pass
        log += line.replace('\n', "<br>")

    if log == "":
        log = "nothing to display<br>"

    return log

#----------------------------[generatehtml]
def generatehtml(logflag):
    html  = "<!docstype html>\r\n"
    html += "<html lang='de'>\r\n"
    html += "<head>\r\n"
    html += "<meta charset='UTF-8'>\r\n"
    html += "<meta name='viewport' content='width=device-width, initial-scale=1'>\r\n"
    html += "<title>PIgc</title>\r\n"
    if logflag == 0:
        html += "<meta http-equiv='refresh' content='10'>\r\n"
    html += "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'>\r\n"
    html += "<link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.1.1/css/all.css' integrity='sha384-O8whS3fhG2OnA5Kas0Y9l3cfpmYjapjI0E4theH4iuMD+pLhbf6JI0jIMfYcK3yZ' crossorigin='anonymous'>\r\n"
    html += "</head>\r\n"
    html += "<body>\r\n"
    html += "<div class='container'>\r\n"
    html += "<main>\r\n"
    if logflag == 0:
        html += "<h2><i class='fab fa-pagelines'></i> PIgc</h2>"
        html += "<p>{:s}</p>".format(time.strftime("%d.%m.%Y %H:%M:%S",time.localtime()))
        html += "<hr>"
        html += "<div class='alert alert-secondary' role='alert'>Temperatur: ?</div>"
        html += "<div class='alert alert-secondary' role='alert'>Regen/Bodenfeuchte: ?</div>"
        html += "<div class='alert alert-secondary' role='alert'>Bewässerung: ?</div>"
        html += "<hr>"
        html += "Verlauf<br>"
        html += "<form action='' method='post'>"
        html += "<div class='btn-group' role='group' aria-label='Basic example'>"
        html += "<button type='submit' class='btn btn-success' name='log1'>Temperatur</button>"
        html += "<button type='submit' class='btn btn-outline-success' name='log2'>Regen</button>"
        html += "<button type='submit' class='btn btn-success' name='log3'>Bodenfeuchte</button>"
        html += "<button type='submit' class='btn btn-outline-success' name='log6'>Logfile</button>"
        html += "</div>"
        html += "</form>"
        html += "<hr>"
        html += "Funktionstests<br>"
        html += "<form action='' method='post'>"
        html += "<div class='btn-group' role='group' aria-label='Basic example'>"
        html += "<button type='submit' class='btn btn-secondary' name='test1'>Kanal 1</button>"
        html += "<button type='submit' class='btn btn-outline-secondary' name='test2'>Kanal 2</button>"
        html += "</div>"
        html += "</form>"
    elif logflag:
        html += "<h2><i class='fas fa-file'></i> Protokolldatei</h2>"
        html += "<form action='' method='post'><button type='submit' class='btn btn-success btn-sm' name='mpage'><i class='fas fa-caret-left'></i> &Uuml;bersicht</button></form>"
        html += "<p><pre>"
        html += readlog(logflag)
        html += "</pre></p>"
        html += "<form action='' method='post'><button type='submit' class='btn btn-success btn-sm' name='mpage'><i class='fas fa-caret-left'></i> &Uuml;bersicht</button></form>"
    html += "\r\n</main>\r\n"
    html += "</div>\r\n"
    html += "</body>\r\n"
    html += "</html>\r\n"
    return html

#----------------------------[RequestHandler]
class RequestHandler(BaseHTTPRequestHandler):
    def resp_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def resp_auth(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def resp_location(self, path):
        self.send_response(302)
        self.send_header('Location', path)
        self.end_headers()

    def senddata(self, data):
        try:
            self.wfile.write(bytes(data, "utf-8"))
        except Exception as e:
            log.info("websvr", "exception! (senddata) {:s} [{:s}]".format(str(e), self.address_string()))

    def resp_page(self, logflag):
        html = generatehtml(logflag)
        self.senddata(html)

    def do_GET2(self):
        if self.path == "/favicon.ico":
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.end_headers()
            self.wfile.write(base64.b64decode(FAVICON))
        else:
            self.resp_header()
            path = str(self.path)
            if path[:4] == "/log" and len(path) >= 5:
                self.resp_page(int(path[4]))
            else:
                self.resp_page(0)

    def do_GET(self):
        global s_key
        if s_key == "":
            self.do_GET2()
        else:
            if self.headers.get('Authorization') == None:
                self.resp_auth()
                self.senddata("no auth header received")
                pass
            elif self.headers.get('Authorization') == "Basic "+s_key:
                self.do_GET2()
                pass
            else:
                self.resp_auth()
                self.senddata("not authenticated")
                pass

    def do_POST2(self):
        content_length = self.headers.get('content-length')
        length = int(content_length[0]) if content_length else 0
        val = str(self.rfile.read(length))

        pos = val.find("log")
        if   pos != -1:
            if pos + 4 < len(val):
                log.info("websvr", "get {:s} [{:s}]".format(val, self.address_string()))
                self.resp_location(val[pos:pos+4])
                return
        self.resp_location("/")

    def do_POST(self):
        global s_key
        if s_key == "":
            self.do_POST2()
        else:
            if self.headers.get('Authorization') == None:
                self.resp_auth()
                self.senddata("no auth header received")
                pass
            elif self.headers.get('Authorization') == "Basic "+s_key:
                self.do_POST2()
                pass
            else:
                self.resp_auth()
                self.senddata("not authenticated")
                pass

#----------------------------[serverthread]
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """

#----------------------------[serverthread]
def serverthread():
    global s_hsvr
    global s_key

    log.info("websvr", "init")

    # init server
    config = configparser.ConfigParser()
    config.read('/usr/local/etc/PIgc.ini')
    try:
        user  = config["WEBSERVER"]["USER"]
        pasw  = config["WEBSERVER"]["PASSWORD"]
    except KeyError:
        user  = ""
        pasw  = ""
        log.info("websvr", "PIgc.ini not filled")

    # authentication
    phrase = user + ":" + pasw
    if len(phrase) > 1:
        s_key = str(base64.b64encode(bytes(phrase, "utf-8")), "utf-8")
    else:
        log.info("websvr", "authentication is disabled")

    # start
    while True:
        try:
            s_hsvr = ThreadedHTTPServer(("", 4711), RequestHandler)
        except Exception:
            time.sleep(1)

        try:
            f = open("/usr/local/etc/PIgc.pem","r")
            f.close()
            try:
                s_hsvr.socket = ssl.wrap_socket(s_hsvr.socket, server_side=True, certfile="/usr/local/etc/PIgc.pem", ssl_version=ssl.PROTOCOL_TLSv1)
                break
            except Exception as e:
                print (str(e))
                s_hsvr.server_close()
                time.sleep(1)
        except Exception:
            log.info("websvr", "https is disabled")
            break

    # running
    log.info("websvr", "started")
    try:
        s_hsvr.serve_forever()
    except KeyboardInterrupt:
        s_hsvr.server_close()
    log.info("websvr", "stop")
    return

#----------------------------[stop]
def stop():
    global s_hsvr
    if s_hsvr != None:
        s_hsvr.shutdown()
    return

#----------------------------[start]
def start():
    thread = threading.Thread(target=serverthread, args=[])
    thread.start()
    return
