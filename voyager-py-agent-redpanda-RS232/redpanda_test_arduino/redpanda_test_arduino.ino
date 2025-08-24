#include <Servo.h>

Servo myservo;

const int LED_PIN = 12;
unsigned long lastQuery = 0;
float TempC;
bool target = false;
bool mesage = false;

void setup() {

  myservo.attach(9);
  
  pinMode(13, OUTPUT);    
  pinMode(12, OUTPUT);
  Serial.begin(9600);
  delay(750);
  myservo.write(110); // move to close
}

void loop() {
  digitalWrite(13, LOW);

int state = (mesage << 1) | target;

switch (state) {
  case 0: // mesage = 0, target = 0
    Serial.println("#bkxiq-haaaa-aaaad-abo5q-cai");
    delay(250);
    break;

  case 1: // mesage = 0, target = 1
    Serial.println("?query");
    break;

  case 2: // mesage = 1, target = 0
    Serial.println("^mail");
    mesage = false;
    break;

  case 3: // mesage = 1, target = 1
    Serial.println("^mail");
    mesage = false;
    break;
}

  delay(500);

  if (Serial.available() > 0) {
    String resp = Serial.readStringUntil('\n');
    resp.trim();

    if (resp == "from:q6kob-gms3g-pmwe2-dwxlt-lctcw-eghzq-xeaag-kvuq2-uezor-64up3-sae:message:open") {
      digitalWrite(12, HIGH);
      myservo.write(0); 
    } else if (resp == "from:q6kob-gms3g-pmwe2-dwxlt-lctcw-eghzq-xeaag-kvuq2-uezor-64up3-sae:message:close") {
      digitalWrite(12, LOW);
      myservo.write(110);
    }
    if(resp == "targetnow"){
      target = true;
    }
    if(resp == "mail_get"){
      mesage = true;
    }
  }
  digitalWrite(13, HIGH);
  delay(5000);
}
