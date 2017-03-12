
#include <Timer.h>
#include <Encoder.h>


// timer 
Timer t;

//motors
int mr1 = 8;
int mr2 = 9;

int ml1 = 10;
int ml2 = 11;


// metal
int metal2 = 12;

int finall = 0;

//ultrasonic
int trig = 6;
int echo = 7;
int duration ;
unsigned dis;

// buzzer
int buz = 13;

// encoder
Encoder knobRight(2, 4);
Encoder knobLeft(3, 5);

long newLeft, newRight;
long positionLeft  = -999;
long positionRight = -999;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // Serial.println("TwoEncoder Test:");

  pinMode(trig, OUTPUT);
  pinMode(ml1, OUTPUT);
  pinMode(ml2, OUTPUT);
  pinMode(mr1, OUTPUT);
  pinMode(mr2, OUTPUT);
  pinMode(buz, OUTPUT);
  t.every(1000, send_data);

}

void loop() {
  t.update();
  
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    char motion = Serial.read();
    movee(motion);
  }
  // ultra metal
  boolean get_ultra = get_ultrasonic();

  boolean met = metal();
  finall = final(get_ultra, met);


  // encoder

  newLeft = knobLeft.read();
  newRight = knobRight.read();
  
  if (newLeft != positionLeft || newRight != positionRight) {
    //Serial.print("Left = ");

    positionLeft = newLeft;
    positionRight = newRight;
  }
}

void send_data()
{
  Serial.print(positionLeft);
  Serial.print(":");
  Serial.print(positionRight);
  Serial.print(":");
  Serial.print(finall);
  Serial.println();
}


void movee(char motion)
{
  switch (motion)
  {
    case 'w':
      forward();
      break;
    case 'd':
      right();
      break;
    case 'a':
      left();
      break;
    case's':
      backward();
      break;
    case'n':
      stopp();
      break;
    case 'z':
      buzz_start();
      break;
    case 'x':
      buzz_stop();
      break;
      // default , backward
  }
}
void buzz_start()
{
  digitalWrite(buz, HIGH);
}

void buzz_stop()
{
  digitalWrite(buz, LOW);
}

void forward()
{
  digitalWrite(mr1, HIGH);
  digitalWrite(mr2, LOW);
  digitalWrite(ml1, HIGH);
  digitalWrite(ml2, LOW);

}
void left()
{
  digitalWrite(ml1, LOW);
  digitalWrite(ml2, HIGH);
  digitalWrite(mr1, HIGH);
  digitalWrite(mr2, LOW);


}
void right()
{
  digitalWrite(ml1, HIGH);
  digitalWrite(ml2, LOW);
  digitalWrite(mr1, LOW);
  digitalWrite(mr2, HIGH);

}
void stopp()
{
  digitalWrite(ml1, LOW);
  digitalWrite(ml2, LOW);
  digitalWrite(mr1, LOW);
  digitalWrite(mr2, LOW);
}
void backward()
{
  digitalWrite(ml1, LOW);
  digitalWrite(ml2, HIGH);
  digitalWrite(mr1, LOW);
  digitalWrite(mr2, HIGH);
}

bool get_ultrasonic()
{
  digitalWrite(trig, HIGH);
  delayMicroseconds(2);
  digitalWrite(trig, LOW);
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  duration = pulseIn(echo, HIGH);
  dis = (duration / 2) / 29.1;
 
  if (dis < 20)
  {
    buzz_start();
    return true;
  }
  else
  {
    buzz_stop();
    return false;
  }
}

bool metal()
{
  int metal_det = digitalRead(metal2);
  // high or 1 ??
  if (metal_det == 1)
  {
    return true;
  }
  else
  {
    return false;
  }
}

int final(boolean ultrasonic , boolean metal)
{

  if (ultrasonic == true)
  {
    buzz_start();
    return 1;
  }
  else if (metal == true)
  {
    buzz_start();
    return 2;
  }
  else
  {

    return 0;
  }

}
