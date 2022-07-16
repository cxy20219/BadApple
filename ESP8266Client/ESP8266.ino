#include <Wire.h>
#include <Adafruit_GFX.h>
#include <ESP8266WiFi.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // 设置OLED宽度,单位:像素
#define SCREEN_HEIGHT 64 // 设置OLED高度,单位:像素

#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define SCL 5
#define SDA 4

#define IP "192.168.43.106"  // 设置连接的ip
#define PORT 50000           // 设置连接的端口

// 连接局域网，设备必须处于同一局域网
const char ssid[] = "nova7pro";      //WiFi名
const char pass[] = "88888888";      //WiFi密码
uint8_t testb[1024] = {};

WiFiClient client;
//初始化WIFI
void initWiFi()
{
  Serial.print("Connecting WiFi...");
  WiFi.mode(WIFI_STA); //配置WIFI为Station模式
  WiFi.begin(ssid, pass); //传入WIFI热点的ssid和密码
  while (WiFi.status() != WL_CONNECTED) //等待连接成功
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); //打印自己的IP地址
  client.connect(IP,PORT);
}

//初始化
void setup()
{
  Serial.begin(9600);
  Serial.println("esp8266 play video");
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  initWiFi();
}

//主循环
void loop()
{
  delay(10);
  while (client.available())
  {
    display.clearDisplay();
    client.read(testb, 1024);
    delay(16);
    display.drawBitmap(0,0,testb,128,64,SSD1306_WHITE);
    display.display();
  }
}
