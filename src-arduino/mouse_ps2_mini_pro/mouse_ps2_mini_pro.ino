#include "PS2Mouse.h"
#define DATA_PIN PD3
#define CLOCK_PIN PD2
#define ACTIVITY_LED 10

PS2Mouse mouse(CLOCK_PIN, DATA_PIN);

void setup() {
  Serial.begin(115200);
  Serial.println("PS2 Mouse handler - 2024");
  pinMode(ACTIVITY_LED, OUTPUT);
  mouse.initialize();
}

void loop() {

  if (Serial.available() > 0) {

    int readByte = Serial.read();    
    if (readByte == 0x48) { digitalWrite(ACTIVITY_LED, HIGH); }
    if (readByte == 0x4C) { digitalWrite(ACTIVITY_LED, LOW); }

    MouseData data = mouse.readData();
    Serial.print(data.status, BIN);
    Serial.print("\tx=");
    Serial.print(data.position.x);
    Serial.print("\ty=");
    Serial.print(data.position.y);
    //Serial.print("\twheel=");
    //Serial.print(data.wheel);
    Serial.println();
  }
  delay(1);
}