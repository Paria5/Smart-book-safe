#include <Keypad.h>
#include "WiFi_NTU.h"
#include <Servo.h>
#include <LiquidCrystal.h>
#include <ThreeWire.h>
#include <RtcDS1302.h>

ThreeWire myWire(9, 10, 8);
RtcDS1302<ThreeWire> Rtc(myWire);

Servo myservo;  // create servo object to control a servo

const int servoPin = 13;
const int buzzerPin = 12;

const byte numRows = 4;
const byte numCols = 4;

char keymap[numRows][numCols] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[numRows] = {31, 33, 35, 37};
byte colPins[numCols] = {39, 41, 43, 45};

Keypad myKeypad = Keypad(makeKeymap(keymap), rowPins, colPins, numRows, numCols);

LiquidCrystal lcd(25, 24, 2, 3, 4, 5);

int incorrectAttempts = 0; // Counter for incorrect password attempts
unsigned long StartTime = 0;
int State=0;

String  Line1="";
String  Line2="";

bool SysSt1=true;
bool SysSt2=true;

String UserName="";
String Password="";
String BufferResponse="";

String extractString(String inputString, String startSubstring, String endSubstring) //call this function whenever you need to extract a substring between two specified substrings
{
  int startPos = inputString.indexOf(startSubstring);
  int endPos = inputString.indexOf(endSubstring);
  
  if (startPos != -1 && endPos != -1) {
    return inputString.substring(startPos + startSubstring.length(), endPos);
  } 
  else 
  {
    return ""; 
  }
}
void setup() {
  Serial.begin(115200);
  Serial1.begin(115200); // Initialize Serial1 for communication with WiFi module
  myservo.attach(servoPin);
  pinMode(buzzerPin, OUTPUT);
  lcd.begin(16, 2);
  //Rtc.Begin();
  String WiFiName = "POCOF4";
  String WiFiPassWord = "876543210";
  WifiSendCommand(WiFiName, WiFiPassWord);
}

void loop() 
{
  if(ReadyToWrite(0))
{
  RtcDateTime now = Rtc.GetDateTime();

  char keypressed = myKeypad.getKey();

  if(keypressed!=NO_KEY)
  {
    /*if((millis()-StartTime)>10000 || !syslinit)
      {
        displayDateTime(now); // Display date and time
      }*/
    if(State==0)
    {
      State=1;
      Line1="1.New User";
      Line2="2.Exsisting User";
      SysSt1=true;
    }
    else if((keypressed=='1' || keypressed=='2')&& State==1)
    {
      WIFIDATAFUNC(String(keypressed)); 
      State=2;
      UserName="";
      Line1="User ID :";
      Line2="";
    }
    else if(State==2)
    {
      Line1="User ID :";          
      Line2=Line2+keypressed;
      
      if(UserName.length()<3)
      {
        UserName=UserName+keypressed;
      }
      else
      {
        UserName=UserName+keypressed;
        WIFIDATAFUNC(UserName); 
        State=3;
        Password="";
        Line1="Password :"; 
        Line2="";
      }
    }
    else if(State==3)
    {
      Line1="Password :";
      Line2=Line2+"*";
      if(Password.length()<3)
      {
          Password=Password+keypressed;
      }
      else
      {
        Password=Password+keypressed;
        WIFIDATAFUNC(Password); 
        State=4;
        Line1="";
        Line2="";
      }
    }
    
    Serial.print("KeyPressed: ");
    Serial.println(keypressed);
    //Serial.print("Line1");
    //Serial.println(Line1);
    //Serial.print("Line2")
    //Serial.println(Line2);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(Line1);
    lcd.setCursor(0, 1);
    lcd.print(Line2);
  }
  if(State==4 && WiFiRecivingData.getSize() > 0)
    {
        BufferResponse = WiFiRecivingData.dequeue();
        String extractedString = extractString(BufferResponse, "abc", "xyz");
        if (extractedString.equals("Exists"))
         {
            Line1="Id Exists";
            Line2=" ";
            State=0;
         }
        if (extractedString.equals("Create"))
         {
            Line1="ACCOUNT CREATED";
            Line2=" ";
            State=0;
         }
         if (extractedString.equals("Incorrect"))
         { 
            State=1;
            Line1="USERID/PASSWORD";
            Line2="INCORRECT ";
            incorrectAttempts++; // Increment incorrect attempts counter
          if(incorrectAttempts >= 3) {

soundAlarm(); // Trigger alarm after 3 incorrect attempts
            incorrectAttempts = 0; // Reset counter after triggering alarm
            State=0;
        }
           
         }
        if (extractedString.equals("Success"))
         {
            Line1="LOGIN ";
            Line2="SUCCESSFULLY ";
            State=0;
            moveServo();
         }
       while(WiFiRecivingData.getSize() > 0)
       WiFiRecivingData.dequeue();
        Serial.print("Wifi Received Value");
        Serial.println(extractedString); 
        Serial.println(BufferResponse);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(Line1);
    lcd.setCursor(0, 1);
    lcd.print(Line2);
    } 
}
  serialEvent1(); // Check for incoming serial data
  WifiUpdate();   // Update WiFi status
  WifiDataRead();
}

void moveServo() 
{  
    myservo.write(90);
    delay(500);
    myservo.write(0);
    delay(100);
}
void soundAlarm() {
  digitalWrite(buzzerPin, HIGH);
  delay(3000);
  digitalWrite(buzzerPin, LOW);
}

void displayDateTime(RtcDateTime now) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Date: ");
  lcd.print(now.Month());
  lcd.print("/");
  lcd.print(now.Day());
  lcd.print("/");
  lcd.print(now.Year());

  lcd.setCursor(0, 1);
  lcd.print("Time: ");
  lcd.print(now.Hour());
  lcd.print(":");
  lcd.print(now.Minute());
  lcd.print(":");
  lcd.print(now.Second());
  delay(200);
}
