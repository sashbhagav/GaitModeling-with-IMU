#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LSM9DS1.h>
#include <Adafruit_Sensor.h>  // not used in this demo but required!

// i2c
Adafruit_LSM9DS1 lsm = Adafruit_LSM9DS1();

#define LSM9DS1_SCK A5
#define LSM9DS1_MISO 12
#define LSM9DS1_MOSI A4
#define LSM9DS1_XGCS 6
#define LSM9DS1_MCS 5


#include <SPI.h>
#include <SD.h>

// Set the pins used
#define cardSelect 4

File logfile;
int x = 0;

// blink out an error code
void error(uint8_t errno) {
  while(1) {
    uint8_t i;
    for (i=0; i<errno; i++) {
      digitalWrite(13, HIGH);
      delay(100);
      digitalWrite(13, LOW);
      delay(100);
    }
    for (i=errno; i<10; i++) {
      delay(200);
    }
  }
}


void setupSensor()
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_2G);
  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS1_MAGGAIN_4GAUSS);
  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS1_GYROSCALE_245DPS);

}


void setup() 
{
  /*Serial.begin(115200);

  while (!Serial) {
    delay(1); // will pause Zero, Leonardo, etc until serial console opens
  }
  
  Serial.println("LSM9DS1 data read demo");
  
  // Try to initialise and warn if we couldn't detect the chip
  if (!lsm.begin())
  {
    Serial.println("Oops ... unable to initialize the LSM9DS1. Check your wiring!");
    while (1);
  }
  Serial.println("Found LSM9DS1 9DOF");

  if (!SD.begin(cardSelect)) {
    Serial.println("Card init. failed!");
    error(2);
  }*/
  char filename[15];
  strcpy(filename, "/ANALOG00.TXT");
  for (uint8_t i = 0; i < 100; i++) {
    filename[7] = '0' + i/10;
    filename[8] = '0' + i%10;
    // create if does not exist, do not open existing, write, sync after write
    if (! SD.exists(filename)) {
      break;
    }
  }

  logfile = SD.open(filename, FILE_WRITE);
  if( ! logfile ) {
    /*Serial.print("Couldnt create "); 
    Serial.println(filename);*/
    //error(3);
  }
  /*Serial.print("Writing to "); 
  Serial.println(filename);*/

  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
  //Serial.println("Ready!");

  // helper to just set the default scaling we want, see above!
  setupSensor();
}

uint8_t i=0;
void loop() 
{
  if (x == 0) {
    x +=1; 
    logfile.println("Josh worst movement yet: Motion data");
  }
  lsm.read();  /* ask it to read in the data */ 

  /* Get a new sensor event */ 
  sensors_event_t a, m, g, temp;

  lsm.getEvent(&a, &m, &g, &temp); 

  //Serial.print("Accel X: "); Serial.print(a.acceleration.x); Serial.print(" m/s^2");
  //Serial.print("\tY: "); Serial.print(a.acceleration.y);     Serial.print(" m/s^2 ");
  //Serial.print("\tZ: "); Serial.print(a.acceleration.z);     Serial.println(" m/s^2 ");
  
  //copying to sd card
  digitalWrite(8, HIGH);
  
  logfile.print(millis());
  logfile.print(", ");
  
  logfile.print(a.acceleration.x);
  logfile.print(", ");
  logfile.print(a.acceleration.y); 
  logfile.print(", ");
  logfile.print(a.acceleration.z); 
  logfile.print(", ");

  logfile.print(m.magnetic.x);
  logfile.print(", "); 
  logfile.print(m.magnetic.y);
  logfile.print(", "); 
  logfile.print(m.magnetic.z);
  logfile.print(", ");

  logfile.print(g.gyro.x);
  logfile.print(", "); 
  logfile.print(g.gyro.y);
  logfile.print(", "); 
  logfile.println(g.gyro.z); 

  logfile.flush();
  digitalWrite(8, LOW);

  //Serial.println();
  delay(200);
}
