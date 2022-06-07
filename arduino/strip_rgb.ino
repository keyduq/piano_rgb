//define pins for the red, green and blue LEDs
#define RED_LED 6
#define BLUE_LED 5
#define GREEN_LED 9
#define BUTTON_PIN 2

String inputData = "";
bool dataComplete = false;
bool firstBoot = true;
const char d[2] = ",";
int red = 255;
int green = 255;
int blue = 255;
bool pressed = false;


void setup() {
  Serial.begin(9600);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  rgbColor(red, green, blue);
  // pinMode(red_light_pin, OUTPUT);
  // pinMode(green_light_pin, OUTPUT);
  // pinMode(blue_light_pin, OUTPUT);
}

void loop() {
  //int buttonState = digitalRead(BUTTON_PIN);
  // if (buttonState == LOW && !pressed) {
  //   // start recording
  //   pressed = true;
  //   Serial.println("b");
  // } else if (pressed && buttonState == HIGH) {
  //   pressed = false;
  // }
  if (dataComplete) {
    processInput(inputData);
    rgbColor(red, green, blue);
    inputData = "";
    dataComplete = false;
  }
}

void rgbColor(int red_light_value, int green_light_value, int blue_light_value) {
  analogWrite(RED_LED, red_light_value);
  analogWrite(GREEN_LED, green_light_value);
  analogWrite(BLUE_LED, blue_light_value);
}
// void rgbColor(int red_light_value, int green_light_value, int blue_light_value)
// {
//   analogWrite(red_light_pin, red_light_value);
//   analogWrite(green_light_pin, green_light_value);
//   analogWrite(blue_light_pin, blue_light_value);
// }

void processInput(String data) {
  char pCh[11];
  strcpy(pCh, data.c_str());

  char * rgb[3];
  int index = 0;
  
  char *token;
  
  token = strtok(pCh, d);
  
  while(token != NULL) {
    rgb[index] = (char *) malloc(strlen(token) + 1);
    strcpy(rgb[index], token);
    
    index++;
    
    token = strtok(NULL, d);
  }
  red = strtol(rgb[0], NULL, 10);
  green = strtol(rgb[1], NULL, 10);
  blue = strtol(rgb[2], NULL, 10);
}

void serialEvent() {
  while(Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      dataComplete = true;
      return;
    }
    inputData += ch;

    // if (ch == -1) {
    //   return;
    // }
    // Serial.write(ch);
    // Serial.print(ch);
    // char *pCh = (char *) malloc(sizeof(ch));
    // *pCh = ch;

    // char *pCh = "20,30,40";
    
    // 


    // Serial.print(rgb[0]);
    // Serial.print(rgb[1]);
    // Serial.print(rgb[2]);
    
  }
}