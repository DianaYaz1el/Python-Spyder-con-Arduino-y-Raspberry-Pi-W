#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "xxx_xx_xxxxxx";  // Cambia esto por tu SSID
const char* password = "xxxxxxxx";  // Cambia esto por tu contraseña

WebServer server(80);

// Pines del puente H
const int ENA = 7;  // GP7 - PWM para Motor 1
const int IN1 = 6;  // GP6
const int IN2 = 5;  // GP5
const int ENB = 2;  // GP2 - PWM para Motor 2
const int IN3 = 4;  // GP4
const int IN4 = 3;  // GP3

void setup() {
  // Configuración de pines
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Conexión WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConexión WiFi establecida");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());

  // Configurar rutas del servidor
  server.on("/adelante", []() {
    digitalWrite(IN1, LOW);  // Cambiado
    digitalWrite(IN2, HIGH); // Cambiado
    digitalWrite(IN3, LOW);  // Cambiado
    digitalWrite(IN4, HIGH); // Cambiado
    analogWrite(ENA, 200);  // Velocidad 80%
    analogWrite(ENB, 200);  // Velocidad 80%
    server.send(200, "text/plain", "Motores avanzando");
  });

  server.on("/atras", []() {
    digitalWrite(IN1, HIGH); // Cambiado
    digitalWrite(IN2, LOW);  // Cambiado
    digitalWrite(IN3, HIGH); // Cambiado
    digitalWrite(IN4, LOW);  // Cambiado
    analogWrite(ENA, 200);  // Velocidad 80%
    analogWrite(ENB, 200);  // Velocidad 80%
    server.send(200, "text/plain", "Motores retrocediendo");
  });

  server.on("/girar_derecha", []() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 200);
    analogWrite(ENB, 200);
    server.send(200, "text/plain", "Giro a la derecha");
  });

  server.on("/girar_izquierda", []() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 200);
    analogWrite(ENB, 200);
    server.send(200, "text/plain", "Giro a la izquierda");
  });

  server.on("/detener", []() {
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);
    server.send(200, "text/plain", "Motores detenidos");
  });

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
}

