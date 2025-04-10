#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>

// Datos de tu red WiFi
const char* ssid = "Diseno_de_Interfaces";
const char* password = "xxxxxxx";

// Configuración del sensor
#define DHTPIN 16        // Pin GPIO (GP16)
#define DHTTYPE DHT11    // Cambia a DHT22 si estás usando ese

DHT dht(DHTPIN, DHTTYPE);
WebServer server(80);

// Página HTML principal
void handleRoot() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  String html = "<h1>Lectura del Sensor DHT11</h1>";
  if (isnan(h) || isnan(t)) {
    html += "<p>Error al leer el sensor</p>";
  } else {
    html += "<p>Temperatura: " + String(t) + " °C</p>";
    html += "<p>Humedad: " + String(h) + " %</p>";
  }

  server.send(200, "text/html", html);
}

// Ruta para interfaz Python (/sensor)
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
  delay(1000);
  Serial.println("Iniciando sensor y WiFi...");
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado a WiFi");
  Serial.print("IP asignada: http://");
  Serial.println(WiFi.localIP());

  // Rutas del servidor web
  server.on("/", handleRoot);
  server.on("/sensor", handleSensorJSON);
  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop() {
  server.handleClient();
}

