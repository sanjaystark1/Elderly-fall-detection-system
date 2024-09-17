

int vs =22; // vibration sensor

void setup(){

pinMode(vs, INPUT);
Serial.begin(9600);

}

void loop(){

long measurement =analogRead(vs);

delay(50);

Serial.println(measurement); 
if (measurement>731)
{ 
  Serial.println("fall is detected "); 
}
}
