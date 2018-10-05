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
fkt_getsensors = None

FAVICON = b"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"

#----------------------------[preparechart]
def preparechart(header, data, twoaxis):
    js ="""
<script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>
<script type='text/javascript'>
    google.charts.load('current', {'packages':['line', 'corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

    var data = google.visualization.arrayToDataTable(["""
    js += header + ",\r\n"
    js += data
    js += "]);\r\n"
    js += """
    var options = {
        legend: { position: 'none' },
        hAxis: { textPosition: 'none' }"""

    if twoaxis == True:
        js += """,
        series: {
          0: {targetAxisIndex: 0},
          1: {targetAxisIndex: 1}
        },
        vAxes: {
          0: {title: 'Temperatur (C)', format: 'decimal', textStyle: {color: '#3366CC'} },
          1: {title: 'Luftfeuchtigkeit', format: 'percent', textStyle: {color: '#DC3912'} }
        }
        """
    else:
        js += """,
        vAxis: {title: 'Temperatur (C)', textStyle: {color: '#3366CC'} }
        """

    js += """
    };

    var materialChart = new google.charts.Line(document.getElementById('chart_div'));
    materialChart.draw(data, google.charts.Line.convertOptions(options));
    }
</script>
"""
    print(js)
    return js

#----------------------------[readdata]
def readdata(compareidx):
    last = ""
    log  = ""
    js   = ""
    min  = [  99.0,  99.0,  99.0 ]
    smi  = list(min)
    max  = [ -99.0, -99.0, -99.0 ]
    sma  = list(max)
    try:
        f = open("/var/log/pigc_data.log","r")
    except Exception:
        try:
            f = open("pigc_data.log","r")
        except Exception:
            return log, js

    data = ""
    dat2 = ""
    ctime = datetime.datetime.today() - datetime.timedelta(days=7)
    sensors = 3
    while True:
        rl = f.readline()
        if not rl:
            break
        line = str(rl)

        try:
            date = datetime.datetime.strptime(line[:13], "%d.%m.%Y %H")
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
                    data += "['{:s}', {:s}, {:f}],\r\n".format(tval, temp, x / 100.0)
                    last = "{:s} {:>5s} &deg;C {:>5s} %<br>".format(tval, temp, humi)
                    log += last
                except:
                    last = "{:s} {:>5s} &deg;C {:>5s} %<br>".format(tval, "-", "-")
                    log += last
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
                    data += "['{:s}', {:s}],\r\n".format(tval, temp)
                    dat2 += "['{:s}', {:s}, {:s}, {:s}],\r\n".format(tval, temp, tem2, tem3)
                    last = "{:s} {:>5s} &deg;C {:>5s} &deg;C {:>5s} &deg;C<br>".format(tval, temp, tem2, tem3)
                    log += last
                except:
                    try:
                        x = float(temp)
                        if x < min[0]:
                            min[0] = x
                        if x > max[0]:
                            max[0] = x
                        data += "['{:s}', {:s}],\r\n".format(tval, temp)
                        last = "{:s} {:>5s} &deg;C<br>".format(tval, temp)
                        log += last
                        sensors = 1
                    except:
                        last = "{:s} {:>5s} &deg;C<br>".format(tval, "-", "-")
                        log += last
        except Exception:
            log += "-<br>"
            pass

    for i in range(len(min)):
        smi[i] = "{:3.1f}".format(min[i])
        sma[i] = "{:3.1f}".format(max[i])

    data  = data.strip(',\r\n')
    data += "\r\n"

    if log == "":
        log = "nothing to display<br>"
    else:
        if min[0] != 99.0:
            if compareidx == 1:
                log = "<b>min:             {:>5s} &deg;C {:>5s} %<br>max:             {:>5s} &deg;C {:>5s} %<br><br></b>".format(smi[0], smi[1], sma[0], sma[1]) + log
                js = preparechart("['Datum', 'Temperatur', 'Luftfeuchtigkeit']", data, True)
            else:
                if sensors == 1:
                    log = "<b>min:             {:>5s} &deg;C<br>max:             {:>5s} &deg;C<br><br></b>".format(smi[0], sma[0]) + log
                    js = preparechart("['Datum', 'Temperatur1']", data, False)
                else:
                    log = "<b>min:             {:>5s} &deg;C {:>5s} &deg;C {:>5s} &deg;C<br>min:             {:>5s} &deg;C {:>5s} &deg;C {:>5s} &deg;C<br><br></b>".format(smi[0], smi[1], smi[2], sma[0], sma[1], sma[2]) + log
                    js = preparechart("['Datum', 'Temperatur1', 'Temperatur2', 'Temperatur3']", dat2, False)
            log = "<i>letzte Messung:<br>{:s}<br></i>".format(last) + log

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
        html += "<meta http-equiv='refresh' content='300'>\r\n"
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
        values = fkt_getsensors()
        html += "<h2><i class='fab fa-pagelines'></i> PIgc</h2>"
        html += "<p>{:s}</p>".format(time.strftime("%d.%m.%Y %H:%M:%S",time.localtime()))
        html += "<hr>"
        html += "<div class='alert alert-secondary' role='alert'>Temperatur: {:s} &deg;C {:s} %</div>".format(values[0], values[1])
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
        if logflag == 1:
            name = "DHT22"
        elif logflag == 2:
            name = "DS1820"
        elif logflag == 3:
            name = "Regen"
        elif logflag == 4:
            name = "Bodenfeuchte"
        else:
            name = "Protokolldatei"
        html += "<h2><i class='fas fa-file'></i> {:s}</h2>".format(name)
        html += "<form action='' method='post'><button type='submit' class='btn btn-success btn-sm' name='mpage'><i class='fas fa-caret-left'></i> &Uuml;bersicht</button></form>"
        if logflag == 1 or logflag == 2:
            html += "<div id='chart_div' style='width: 700px; height: 350px'></div>"
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
def start(fgetsensors):
    global fkt_getsensors

    fkt_getsensors = fgetsensors

    thread = threading.Thread(target=serverthread, args=[])
    thread.start()
    return
