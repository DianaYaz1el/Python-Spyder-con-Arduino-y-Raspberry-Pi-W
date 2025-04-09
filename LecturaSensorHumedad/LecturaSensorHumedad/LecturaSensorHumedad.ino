#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>

#define DHTPIN 16       // GP16 en la Pico W
#define DHTTYPE DHT11   // Sensor DHT11

const char* ssid = "Diseno_de_Interfaces";   // Cambia a tu red
const char* password = "xxxxxxxx";           // Cambia tu contraseña

DHT dht(DHTPIN, DHTTYPE);
WebServer server(80);

void handleRoot() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  String pagina = "<h1>Lectura de Sensor DHT11</h1>";

  if (isnan(h) || isnan(t)) {
    pagina += "<p>Error al leer el sensor</p>";
  } else {
    pagina += "<p>Temperatura: " + String(t) + " °C</p>";
    pagina += "<p>Humedad: " + String(h) + " %</p>";
  }

  server.send(200, "text/html", pagina);
}

void handleSensorJSON() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    server.send(500, "application/json", "{\"error\":\"Lectura fallida\"}");
  } else {
    String json = "{\"temp\":" + String(t, 2) + ",\"hum\":" + String(h, 2) + "}";
    server.send(200, "application/json", json);
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado a WiFi");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/sensor", handleSensorJSON);
  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop() {
  server.handleClient();
}
