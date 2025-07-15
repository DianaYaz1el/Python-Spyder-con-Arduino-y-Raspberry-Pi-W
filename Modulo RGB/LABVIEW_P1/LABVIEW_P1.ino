// Pines del LED RGB
const int pinRojo = 2;
const int pinVerde = 3;
const int pinAzul = 4;

void setup() {
  pinMode(pinRojo, OUTPUT);
  pinMode(pinVerde, OUTPUT);
  pinMode(pinAzul, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char comando = Serial.read();

    // Apagar todos antes de encender el que se requiere
    digitalWrite(pinRojo, LOW);
    digitalWrite(pinVerde, LOW);
    digitalWrite(pinAzul, LOW);

    if (comando == 'R') {
      digitalWrite(pinRojo, HIGH);
    } 
    else if (comando == 'G') {
      digitalWrite(pinVerde, HIGH);
    } 
    else if (comando == 'B') {
      digitalWrite(pinAzul, HIGH);
    } 
    else if (comando == 'X') {
      // X apaga todos explícitamente
      digitalWrite(pinRojo, LOW);
      digitalWrite(pinVerde, LOW);
      digitalWrite(pinAzul, LOW);
    }
  }
}
