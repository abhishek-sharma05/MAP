#include <Servo.h>

#define BASE_PIN 2
#define ARM_PIN 3
#define CLAW_PIN 4

const int BASE_LENGTH = 10;  // length of base link
const int ARM_LENGTH = 15;  // length of arm link
const int FOREARM_LENGTH = 20;  // length of forearm link

Servo clawServo;

void setup() {
  Serial.begin(9600);
  pinMode(BASE_PIN, OUTPUT);
  pinMode(ARM_PIN, OUTPUT);
  clawServo.attach(CLAW_PIN);
}

void loop() {
  // Sample XY coordinates to go to
  float x = 10.0;
  float y = 20.0;
  float z = 30.0;

  // Compute angles for the 3R manipulator
  float baseAngle = atan2(y, x);
  float r = sqrt(x*x + y*y);
  float forearmAngle = acos((r*r + z*z - ARM_LENGTH*ARM_LENGTH - FOREARM_LENGTH*FOREARM_LENGTH) / (2 * ARM_LENGTH * FOREARM_LENGTH));
  float armAngle = atan2(z, r) + atan2(FOREARM_LENGTH * sin(forearmAngle), ARM_LENGTH + FOREARM_LENGTH * cos(forearmAngle));

  // Convert angles to servo positions
  int basePos = map(baseAngle, -PI, PI, 0, 180);
  int armPos = map(armAngle, -PI, PI, 0, 180);
  int clawPos = 90; // Default closed position

  // Move the manipulator to the desired position
  digitalWrite(BASE_PIN, basePos);
  digitalWrite(ARM_PIN, armPos);
  clawServo.write(clawPos);

  // Wait for the manipulator to reach the desired position
  delay(1000);

  // Open the claw to pick up the cylinder
  clawPos = 0;
  clawServo.write(clawPos);
  delay(1000);

  // Move the cylinder behind the manipulator
  digitalWrite(BASE_PIN, basePos - 90);
  delay(1000);

  // Close the claw to hold the cylinder
  clawPos = 90;
  clawServo.write(clawPos);
  delay(1000);

  // Move the cylinder to the desired location
  digitalWrite(BASE_PIN, basePos + 90);
  delay(1000);

  // Release the cylinder by opening the claw
  clawPos = 0;
  clawServo.write(clawPos);
  delay(1000);
}
