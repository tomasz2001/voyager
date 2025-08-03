const int LED_PIN = 12;
unsigned long lastQuery = 0;
const unsigned long QUERY_INTERVAL = 1000; // ms

void setup() {
  pinMode(13, OUTPUT);    // wskaźnik aktywności
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // 1) migajemy diodą 13, żeby było widać, że kod działa
  digitalWrite(13, millis() % 200 < 100 ? HIGH : LOW);

  unsigned long now = millis();
  // 2) co sekundę wysyłamy zapytanie do Pythona
  if (now - lastQuery >= QUERY_INTERVAL) {
    lastQuery = now;
    Serial.println("?led");
  }

  // 3) jeśli przyszła jakaś linia z Pythona – czytamy i reagujemy
  if (Serial.available() > 0) {
    String resp = Serial.readStringUntil('\n');
    resp.trim();
    if (resp == "on") {
      digitalWrite(LED_PIN, HIGH);
    } else if (resp == "off") {
      digitalWrite(LED_PIN, LOW);
    }
    // jeśli dostaniesz coś innego – możesz np. printować do debugu
  }
}
