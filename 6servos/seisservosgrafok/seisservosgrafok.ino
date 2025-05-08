#include <Servo.h>

Servo servos[6];
int pins[6] = {3, 5, 6, 9, 10, 11};
int currentAngles[6] = {90, 90, 30, 180, 90, 90};

// Joysticks
const int joyPins[4] = {A0, A1, A2, A3};  // X1, Y1, X2, Y2
const int servoMap[4] = {0, 1, 2, 3};     // Qué servo controla cada eje

// Zona muerta y paso
const int deadZone = 80;
const int step = 2;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 6; i++) {
    servos[i].attach(pins[i]);
    servos[i].write(currentAngles[i]);
  }
}

void loop() {
  // 1. Leer joystick para 4 servos
  for (int i = 0; i < 4; i++) {
    controlarEje(joyPins[i], servoMap[i]);
  }

  // 2. Escuchar comandos de MATLAB (6 ángulos separados por comas)
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    char buffer[64];
    input.toCharArray(buffer, sizeof(buffer));
    char* token = strtok(buffer, ",");

    int angles[6];
    int index = 0;

    while (token != NULL && index < 6) {
      angles[index] = constrain(atoi(token), 0, 180);
      token = strtok(NULL, ",");
      index++;
    }

    if (index == 6) {
      for (int i = 0; i < 6; i++) {
        moverSuave(i, angles[i]);
        currentAngles[i] = angles[i];
      }
    } else {
      Serial.println("Error: se esperaban 6 valores.");
    }
  }

  // 3. (Opcional) Enviar ángulos actuales a MATLAB
  static unsigned long lastSend = 0;
  if (millis() - lastSend > 100) {
    String estado = String(currentAngles[0]);
    for (int i = 1; i < 6; i++) {
      estado += "," + String(currentAngles[i]);
    }
    Serial.println(estado);
    lastSend = millis();
  }

  delay(10);  // Pequeña pausa para estabilidad
}

void controlarEje(int pin, int servoID) {
  int lectura = analogRead(pin);
  int diferencia = lectura - 512;

  if (abs(diferencia) > deadZone) {
    int cambio = map(diferencia, -512, 512, -step, step);
    int nuevoAngulo = constrain(currentAngles[servoID] + cambio, 0, 180);
    moverSuave(servoID, nuevoAngulo);
    currentAngles[servoID] = nuevoAngulo;
  }
}

void moverSuave(int servoID, int destino) {
  int actual = currentAngles[servoID];
  if (actual == destino) return;

  int paso = (actual < destino) ? 1 : -1;
  for (int pos = actual; pos != destino; pos += paso) {
    servos[servoID].write(pos);
    delay(5);
  }
  servos[servoID].write(destino);
}
