const int pinSensorDigital = 7;    // D0 del sensor de flama
const int pinSensorAnalogico = A0; // A0 del sensor de flama
const int pinLED = 8;              // LED conectado al pin 8

bool lecturaActiva = false;

void setup() {
  pinMode(pinSensorDigital, INPUT);
  pinMode(pinSensorAnalogico, INPUT);
  pinMode(pinLED, OUTPUT);
  Serial.begin(9600);
  Serial.println("Esperando comando 'L' para empezar a leer...");
}

void loop() {
  // Revisa si llega un comando
  if (Serial.available()) {
    char comando = Serial.read();
    if (comando == 'L') {
      lecturaActiva = true;
      Serial.println("Lectura activada.");
      delay(100);  // Pequeño delay para dar tiempo a la interfaz
    } else if (comando == 'S') {
      lecturaActiva = false;
      digitalWrite(pinLED, LOW);
      Serial.println("Lectura detenida.");
    }
  }

  // Si está activa la lectura
  if (lecturaActiva) {
    int fuegoDigital = digitalRead(pinSensorDigital);
    int valorAnalogico = analogRead(pinSensorAnalogico);  // 0 a 1023

    Serial.print("A0:");
    Serial.println(valorAnalogico);  // Para que LabVIEW pueda identificarlo

    if (fuegoDigital == LOW) {
      digitalWrite(pinLED, HIGH);
      Serial.println("SIN FUEGO");
    } else {
      digitalWrite(pinLED, LOW);
      Serial.println("FUEGO DETECTADO");
    }

    delay(200);  // Tiempo entre lecturas
  }
}

