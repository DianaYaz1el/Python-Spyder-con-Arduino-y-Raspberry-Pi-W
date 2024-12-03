#include <WiFi.h>
#include <WebServer.h>

// Configuración WiFi
const char* ssid = "XXXXXXXX";  // Tu SSID
const char* password = "XXXXXXXX";          // Tu contraseña
WebServer server(80);

// Pines de los LEDs
const int ledVerde = 14; //GP14  // Ajusta los pines según tus conexiones
const int ledRojo = 15; //GP15 
const int ledAzul = 16; //GP16 

// Variables de estado de los LEDs
bool estadoLEDVerde = false;
bool estadoLEDRojo = false;
bool estadoLEDAzul = false;

// Funciones para manejar el toggle de los LEDs
void handleLEDToggleVerde() {
  estadoLEDVerde = !estadoLEDVerde;
  digitalWrite(ledVerde, estadoLEDVerde ? HIGH : LOW);
  server.send(200, "text/plain", estadoLEDVerde ? "LED Verde encendido" : "LED Verde apagado");
}

void handleLEDToggleRojo() {
  estadoLEDRojo = !estadoLEDRojo;
  digitalWrite(ledRojo, estadoLEDRojo ? HIGH : LOW);
  server.send(200, "text/plain", estadoLEDRojo ? "LED Rojo encendido" : "LED Rojo apagado");
}

void handleLEDToggleAzul() {
  estadoLEDAzul = !estadoLEDAzul;
  digitalWrite(ledAzul, estadoLEDAzul ? HIGH : LOW);
  server.send(200, "text/plain", estadoLEDAzul ? "LED Azul encendido" : "LED Azul apagado");
}

void setup() {
  Serial.begin(115200);

  // Configurar pines de los LEDs como salida
  pinMode(ledVerde, OUTPUT);
  pinMode(ledRojo, OUTPUT);
  pinMode(ledAzul, OUTPUT);

  // Asegurarse de que los LEDs estén apagados inicialmente
  digitalWrite(ledVerde, LOW);
  digitalWrite(ledRojo, LOW);
  digitalWrite(ledAzul, LOW);

  // Conexión a WiFi
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

  // Configuración de rutas para el servidor web
  server.on("/verdetoggle", handleLEDToggleVerde);
  server.on("/rojotoggle", handleLEDToggleRojo);
  server.on("/azultoggle", handleLEDToggleAzul);

  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop() {
  server.handleClient();
}
