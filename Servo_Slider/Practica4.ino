#include <WiFi.h>
#include <WebServer.h>
#include <Servo.h>

// Configuración WiFi
const char* ssid = "Dxxxx_de_xxxxx";  // Cambia esto por tu SSID
const char* password = "xxxxxxx";          // Cambia esto por tu contraseña

// Configuración del Servomotor
Servo servo;
const int servoPin = 17;  // Cambia este pin si usas otro
int angulo = 90;          // Ángulo inicial del servo

// Definir pulsos mínimos y máximos para el servo (en microsegundos)
const int pulsoMin = 500;   // Pulso mínimo (ajusta según las especificaciones de tu servo)
const int pulsoMax = 2500;  // Pulso máximo (ajusta según las especificaciones de tu servo)

// Crear el servidor web en el puerto 80
WebServer server(80);

// Función para manejar la página principal
void handleRoot() {
  String pagina = "<h1>Control de Servomotor</h1>"
                  "<form action='/mover'>"
                  "Ángulo (0-180): <input type='number' name='angulo' min='0' max='180' value='" + String(angulo) + "'>"
                  "<button type='submit'>Mover Servo</button>"
                  "</form>";
  server.send(200, "text/html", pagina);
}

// Función para manejar el movimiento del servo
void handleMover() {
  if (server.hasArg("angulo")) {
    angulo = server.arg("angulo").toInt();
    angulo = constrain(angulo, 0, 180); // Asegurar que el ángulo esté en el rango permitido
    servo.write(angulo);                // Mover el servo al ángulo especificado
    Serial.println("Ángulo ajustado a: " + String(angulo));
    String respuesta = "<h1>Servo movido</h1>"
                       "<p>El servo se movió a " + String(angulo) + " grados.</p>"
                       "<a href='/'>Volver</a>";
    server.send(200, "text/html", respuesta);
  } else {
    server.send(400, "text/html", "Parámetro 'angulo' faltante.");
  }
}

void setup() {
  Serial.begin(115200);

  // Conexión WiFi
  Serial.print("Conectando a WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConexión WiFi establecida");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());

  // Configurar el servo con pulsos mínimos y máximos
  servo.attach(servoPin, pulsoMin, pulsoMax);
  servo.write(angulo);  // Posicionar el servo en el ángulo inicial

  // Configuración del servidor
  server.on("/", handleRoot);          // Página principal
  server.on("/mover", handleMover);    // Mover el servo
  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop() {
  server.handleClient(); // Manejar las solicitudes del cliente
}

