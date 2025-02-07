#include <SoftwareSerial.h>

SoftwareSerial bluetooth(0, 1); // RX, TX para el módulo HC-06

const int sensorPinVoltaje = A0;  // Pin del sensor de voltaje
const int sensorPinCorriente = A1; // Pin del sensor ACS712
const float sensibilidad = 0.185;  // Sensibilidad del ACS712 (en V/A) - Ajusta según tu modelo
const int offset = 512;            // Valor de salida del ACS712 sin corriente (ajústalo según tu sensor)

const float R1 = 2000.0;   // Resistencia R1 en ohmios (2kΩ)
const float R2 = 1500.0;   // Resistencia R2 en ohmios (1.5kΩ)
const float maxADC = 1023.0; // Valor máximo del ADC (10 bits)
const float Vref = 5.0;   // Voltaje de referencia del Arduino

void setup() {
    bluetooth.begin(9600);   // Comunicación con el HC-06
    Serial.begin(9600);      // Comunicación con el Monitor Serial
    Serial.println("Inicializando Bluetooth y sensores...");
}

void loop() {
    // Leer voltaje del divisor
    int rawVoltaje = analogRead(sensorPinVoltaje);
    float Vout = rawVoltaje * (Vref / maxADC);
    float voltaje = (Vout * ((R1 + R2) / R2)) * 2.45;

    // Leer corriente del ACS712
    int rawCorriente = analogRead(sensorPinCorriente);
    float corriente = (rawCorriente - offset) * (Vref / maxADC) / sensibilidad;

    // Enviar datos por Bluetooth en formato CSV
    bluetooth.print(voltaje);
    bluetooth.print(",");
    bluetooth.println(corriente);

    // También enviar al Monitor Serial para depuración
    Serial.print("Voltaje: ");
    Serial.print(voltaje);
    Serial.print(" V, Corriente: ");
    Serial.print(corriente);
    Serial.println(" A");

    delay(1000); // Enviar datos cada segundo
}
