const int LED_PIN = 12;
unsigned long lastQuery = 0;
float TempC;
bool target = false;
bool mesage = false;

void setup() {

  pinMode(13, OUTPUT);    
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  delay(1500);
  

}

void loop() {
  digitalWrite(13, LOW);
  delay(500);
  digitalWrite(13, HIGH);

  if (target == true) {
    lastQuery = now;
    Serial.println("?query");
    if (mesage == true){
      Serial.println("^mail");
      mesage = false;
    }
    
  }else{
    Serial.println("#mh2ii-qqaaa-aaaae-aakpa-cai")
  }
  delay(1000);

  if (Serial.available() > 0) {
    String resp = Serial.readStringUntil('\n');
    resp.trim();
    if (resp == "on") {
      digitalWrite(LED_PIN, HIGH);
    } else if (resp == "off") {
      digitalWrite(LED_PIN, LOW);
    }
    if(resp == "targetnow"){
      target = true;
    }
    if(resp == "mail_get"){
      mesage = true;
    }
  }
  delay(1000);
}
