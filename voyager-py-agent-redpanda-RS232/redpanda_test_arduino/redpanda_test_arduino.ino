const int LED_PIN = 12;
unsigned long lastQuery = 0;
float TempC;

void setup() {
  pinMode(13, OUTPUT);    
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(13, LOW);
  delay(500);
  digitalWrite(13, HIGH);
  unsigned long now = millis();
  if (now - lastQuery >= QUERY_INTERVAL) {
    lastQuery = now;
    Serial.println("?led");
    delay(1000);
    TempC = Read_NTC10k();
    Serial.print("^");
    Serial.println(TempC, 2);
  }


  if (Serial.available() > 0) {
    String resp = Serial.readStringUntil('\n');
    resp.trim();
    if (resp == "on") {
      digitalWrite(LED_PIN, HIGH);
    } else if (resp == "off") {
      digitalWrite(LED_PIN, LOW);
    }
  }
}

float Read_NTC10k()
{
  float a = 639.5, b = -0.1332, c = -162.5;
  float Rntc, Vntc, Temp;
  Vntc = (analogRead(A0)*5.0)/1023.0;
  Rntc = 10000.0 * ((5.0/Vntc) - 1);
  Temp = a * pow(Rntc, b) + c;
  return Temp;
}
