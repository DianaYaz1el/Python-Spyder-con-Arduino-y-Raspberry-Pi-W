#include <WiFi.h>
#include <WebServer.h>

// Configuración WiFi
const char* ssid = "xxxx_xx_xxxx";
const char* password = "xxxxxxxx";
WebServer server(80); // Servidor web en el puerto 80

void handleRoot() {
  server.send(200, "text/plain", "Servidor Pico W activo");
}

void handleLEDOn() {
  digitalWrite(LED_BUILTIN, HIGH);
  server.send(200, "text/plain", "LED encendido");
}

void handleLEDOff() {
  digitalWrite(LED_BUILTIN, LOW);
  server.send(200, "text/plain", "LED apagado");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  // Conectar al WiFi
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado al WiFi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());

  // Configurar rutas del servidor web
  server.on("/", handleRoot);
  server.on("/ledon", handleLEDOn);
  server.on("/ledoff", handleLEDOff);

  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop() {
  server.handleClient();
}
