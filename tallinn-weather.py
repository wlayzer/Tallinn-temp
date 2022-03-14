import http.server
import prometheus_client as prom
from prometheus_client import start_http_server
import requests
import json
import time

api_key = ""
region = "Tallinn"
units = "metric"
url = "https://api.openweathermap.org/data/2.5/weather?q=%s&units=%s&APPID=%s" % (region, units, api_key)

tallinn_temp_gauge = prom.Gauge('tallinn_temp', 'Tallinn temperature')

def get_temp():
 while True:
  response = requests.get(url)
  data = json.loads(response.text)
  current_temp = data["main"]["temp"]
  tallinn_temp_gauge.set(current_temp)
  time.sleep(60)

class ServerHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"potato")

if __name__ == "__main__":
  start_http_server(8000)
  server = http.server.HTTPServer(('', 8001), ServerHandler)
  get_temp()
  print("Prometheus metrics available on port 8000 /metrics")
  #print("HTTP server available on port 8001")
  server.serve_forever()
