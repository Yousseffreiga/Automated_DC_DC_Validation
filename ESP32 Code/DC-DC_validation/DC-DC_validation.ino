// ADC pins
const int ADC_DC_Input = 4;
const int ADC_DC_Output = 5;

// GPIO controlling transistor/load
const int LOAD_SWITCH_PIN = 6;

// Voltage divider resistor values
const float R1 = 100000.0; // 100k ohm
const float R2 = 10000.0;  // 10k ohm

// Divider ratio = 11
const float DRatio = (R1 + R2) / R2;

// ADC reference approximation
const float ADC_REF_VOLTAGE = 3.30;

// Number of samples to average
const int NUM_SAMPLES = 20;

void setup() {
  Serial.begin(115200);
  delay(1000);

  analogReadResolution(12); // 0 to 4095

  analogSetPinAttenuation(ADC_DC_Input, ADC_11db);
  analogSetPinAttenuation(ADC_DC_Output, ADC_11db);

  pinMode(ADC_DC_Input, INPUT);
  pinMode(ADC_DC_Output, INPUT);

  pinMode(LOAD_SWITCH_PIN, OUTPUT);
  digitalWrite(LOAD_SWITCH_PIN, LOW);

  Serial.println("LM2596S DC-DC Converter Validation Monitor");
  Serial.println("------------------------------------------");
}

void loop() {
  // Test with load OFF
  digitalWrite(LOAD_SWITCH_PIN, LOW);
  delay(1000); // let voltage settle
  Serial.println("LOAD OFF");
  readAndPrintVoltage();

  // Test with load ON
  digitalWrite(LOAD_SWITCH_PIN, HIGH);
  delay(1000); // let voltage settle
  Serial.println("LOAD ON");
  readAndPrintVoltage();

  delay(3000);
}

int readAverageADC(int pin) {
  long total = 0;

  for (int i = 0; i < NUM_SAMPLES; i++) {
    total += analogRead(pin);
    delay(2);
  }

  return total / NUM_SAMPLES;
}

void readAndPrintVoltage() {
  int rawInput = readAverageADC(ADC_DC_Input);
  int rawOutput = readAverageADC(ADC_DC_Output);

  // Convert raw ADC reading to voltage at ESP32 ADC pin
  float inputAdcVoltage = (rawInput / 4095.0) * ADC_REF_VOLTAGE;
  float outputAdcVoltage = (rawOutput / 4095.0) * ADC_REF_VOLTAGE;

  // Convert ADC pin voltage back to actual measured voltage
  float dcInputVoltage = inputAdcVoltage * DRatio;
  float dcOutputVoltage = outputAdcVoltage;

  Serial.print("Input ADC Raw: ");
  Serial.print(rawInput);
  Serial.print(" | ADC Pin Voltage: ");
  Serial.print(inputAdcVoltage, 3);
  Serial.print(" V | Input Voltage: ");
  Serial.print(dcInputVoltage, 2);
  Serial.println(" V");

  Serial.print("Output ADC Raw: ");
  Serial.print(rawOutput);
  Serial.print(" | ADC Pin Voltage: ");
  Serial.print(outputAdcVoltage, 3);
  Serial.print(" V | Output Voltage: ");
  Serial.print(dcOutputVoltage, 2);
  Serial.println(" V");

  Serial.println("----------------------");
}