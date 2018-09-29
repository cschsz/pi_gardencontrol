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

#----------------------------[preparechart]
def preparechart(header, data):
    js = "\
<script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>\r\n\
<script type='text/javascript'>\r\n\
    google.charts.load('current', {'packages':['corechart']});\r\n\
    google.charts.setOnLoadCallback(drawChart);\r\n\
    function drawChart() {\r\n\
    var data = google.visualization.arrayToDataTable([\r\n"
    js += header + ",\r\n"
    js += data + "\r\n"
    js += "]);\r\n\
    \r\n\
    var options = {\r\n\
        title: 'Temperaturverlauf',\r\n\
        curveType: 'function',\r\n\
        legend: { position: 'none' },\r\n\
        hAxis: { textPosition: 'none' }\r\n\
    };\r\n\
    \r\n\
    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));\r\n\
    chart.draw(data, options);\r\n\
    }\r\n\
</script>\r\n"
    return js

#----------------------------[readdata]
def readdata(compareidx):
    log = ""
    js  = ""
    min = [  99.0,  99.0,  99.0 ]
    max = [ -99.0, -99.0, -99.0 ]
    try:
        f = open("/var/log/pigc_data.log","r")
    except Exception:
        try:
            f = open("pigc_data.log","r")
        except Exception:
            return log, js

    data = ""
    dat2 = ""
    ctime = datetime.datetime.today() - datetime.timedelta(days=15)
    sensors = 3
    while True:
        rl = f.readline()
        if not rl:
            break
        line = str(rl)

        try:
            date = datetime.datetime.strptime(line[:10], "%d.%m.%Y")
            if date < ctime:
                continue
        except Exception:
            pass

        values = line.split(";")
        try:
            tval = values[0]
            if compareidx == 1:
                temp = values[1]
                humi  = values[2]
                try:
                    x = float(temp)
                    if x < min[0]:
                        min[0] = x
                    if x > max[0]:
                        max[0] = x
                    x = float(humi)
                    if x < min[1]:
                        min[1] = x
                    if x > max[1]:
                        max[1] = x
                    data += "['{:s}', {:s}, {:s}],\r\n".format(tval[:16], temp, humi)
                    log += "{:s} {:>5s} &deg;C {:>5s} %<br>".format(tval, temp, humi)
                except:
                    log += "{:s} {:>5s} &deg;C {:>5s} %<br>".format(tval, "-", "-")
            else:
                temp = values[3]
                tem2 = values[4]
                tem3 = values[5]
                try:
                    x = float(temp)
                    if x < min[0]:
                        min[0] = x
                    if x > max[0]:
                        max[0] = x
                    x = float(tem2)
                    if x < min[1]:
                        min[1] = x
                    if x > max[1]:
                        max[1] = x
                    x = float(tem3)
                    if x < min[2]:
                        min[2] = x
                    if x > max[2]:
                        max[2] = x
                    data += "['{:s}', {:s}],\r\n".format(tval[:16], temp)
                    dat2 += "['{:s}', {:s}, {:s}, {:s}],\r\n".format(tval[:16], temp, tem2, tem3)
                    log += "{:s} {:>5s} &deg;C {:>5s} &deg;C {:>5s} &deg;C<br>".format(tval, temp, tem2, tem3)
                except:
                    try:
                        x = float(temp)
                        if x < min[0]:
                            min[0] = x
                        if x > max[0]:
                            max[0] = x
                        data += "['{:s}', {:s}],\r\n".format(tval[:16], temp)
                        log += "{:s} {:>5s} &deg;C<br>".format(tval, temp)
                        sensors = 1
                    except:
                        log += "{:s} {:>5s} &deg;C<br>".format(tval, "-", "-")
        except Exception:
            log += "-<br>"
            pass

    data  = data.strip(',\r\n')
    data += "\r\n"
    if compareidx == 1:
        if min != 99.0:
            smi1 = "{:3.1f}".format(min[0])
            sma1 = "{:3.1f}".format(max[0])
            smi2 = "{:3.1f}".format(min[1])
            sma2 = "{:3.1f}".format(max[1])
            log = "<b>min:             {:>5s} &deg;C {:>5s} %<br>min:             {:>5s} &deg;C {:>5s} %<br><br></b>".format(smi1, smi2, sma1, sma2) + log
        js = preparechart("['Datum', 'Temperatur', 'Humidity']", data)
    else:
        if sensors == 1:
            if min != 99.0:
                smi1 = "{:3.1f}".format(min[0])
                sma1 = "{:3.1f}".format(max[0])
                log = "<b>min:             {:>5s} &deg;C<br>min:             {:>5s} &deg;C<br><br></b>".format(smi1, sma1) + log
            js = preparechart("['Datum', 'Temperatur1']", data)
        else:
            if min != 99.0:
                smi1 = "{:3.1f}".format(min[0])
                sma1 = "{:3.1f}".format(max[0])
                smi2 = "{:3.1f}".format(min[1])
                sma2 = "{:3.1f}".format(max[1])
                smi3 = "{:3.1f}".format(min[2])
                sma3 = "{:3.1f}".format(max[2])
                log = "<b>min:             {:>5s} &deg;C {:>5s} &deg;C {:>5s} &deg;C<br>min:             {:>5s} &deg;C {:>5s} &deg;C {:>5s} &deg;C<br><br></b>".format(smi1, smi2, smi3, sma1, sma2, sma3) + log
            js = preparechart("['Datum', 'Temperatur1', 'Temperatur2', 'Temperatur3']", dat2)

    if log == "":
        log = "nothing to display<br>"

    return log, js

#----------------------------[readlog]
def readlog(logflag):
    if   logflag == 1:
        return readdata(1)
    elif logflag == 2:
        return readdata(2)
    elif logflag == 3:
        return "nothing to display<br>", ""
    elif logflag == 4:
        return "nothing to display<br>", ""
    else:
        log = ""
        compare = " "

    ctime = datetime.datetime.today() - datetime.timedelta(days=4)
    try:
        f = open("/var/log/pigc_{:s}.log".format(time.strftime("%Y-%m")),"r")
    except Exception:
        try:
            f = open("pigc_{:s}.log".format(time.strftime("%Y-%m")),"r")
        except Exception:
            return "no log found", ""

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

    return log, ""

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
    else:
        hlog, hjs = readlog(logflag)
        if logflag == 1 or logflag == 2:
            html += hjs
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
        html += "<button type='submit' class='btn btn-success' name='log1'>DHT22</button>"
        html += "<button type='submit' class='btn btn-outline-success' name='log2'>DS1820</button>"
        html += "<button type='submit' class='btn btn-success' name='log3'>Regen</button>"
        html += "<button type='submit' class='btn btn-outline-success' name='log4'>Boden</button>"
        html += "<button type='submit' class='btn btn-success' name='log6'>Logfile</button>"
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
    else:
        html += "<h2><i class='fas fa-file'></i> Protokolldatei</h2>"
        html += "<form action='' method='post'><button type='submit' class='btn btn-success btn-sm' name='mpage'><i class='fas fa-caret-left'></i> &Uuml;bersicht</button></form>"
        if logflag == 1 or logflag == 2:
            html += "<div id='curve_chart' style='width: 600px; height: 300px'></div>"
        html += "<p><pre>"
        html += hlog
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
