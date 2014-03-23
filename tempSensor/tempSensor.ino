#include "DHT.h"

#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT11   // DHT 11 

// Connect pin 1 (on the left) of the sensor to +5V
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND

DHT dht(DHTPIN, DHTTYPE);

int Stat = 13;
int bufferwait = 250;
int loopwait = 1000;
String transmit = String('x');

void setup() {
  Serial.begin(9600); 
  //Serial.println("DHTxx test!");
  dht.begin();
}

void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  int h = dht.readHumidity();
  int t = dht.readTemperature();

  digitalWrite(Stat,HIGH);
  transmit = String(h,DEC)+String(",")+String(t,DEC); 
  Serial.println(transmit);
  delay(bufferwait);
  digitalWrite(Stat,LOW);
  delay(loopwait);
}
