---
name: "测试 skills"
---
# 1. 查询所有微服务信息,router_to为空时,为对服务中心进行操作
```json
{
  "router_to":"",
  "operation":"query",
  "slice_len":0,
  "body":{}
}
```
# 2. 启动 wgc 屏幕捕获
```json
{
  "router_to":"run_service_name",
  "operation":"wgc",
  "slice_len":0,
  "body":{
    "target":"target_name"
  }
}
```
# 3. 获取同步ocr结果
## 1. 其中threshold为识别阈值,默认0.8,可选,更多选项后续会开放
```json
{
  "router_to":"run_service_name",
  "operation":"ocr",
  "slice_len":0,
  "body":{
    "threshold":0.8
    
  }
}
```
# 4. win32输入操作
## 1. 其中target为目标窗口名称,
## 2. 输入按键时请以大写字母字符或者字符串作为key,例如"ESC","A"等
```json
{
  "router_to":"run_service_name",
  "operation":"win32_input",
  "slice_len":0,
  "body":{
    "target":"target_name",
    "inputs":[
      {
        "type":"move_mouse",
        "x":1173,
        "y":600
      },
      {
        "type":"click_mouse",
        "click_name":"left_click",
        "count":1
      },
      {
        "type":"send_input",
        "key":"ESC",
        "duration":1000
      }
    ]
  }
}
`````

# 5. yolo模型调用
## 1. yolo模型查询
```json
{
  "router_to":"run_service_name",
  "operation":"get_yolo_model",
  "slice_len":0,
  "body":{

  }
}
```
## 2. yolo模型调用
```json
{
  "router_to":"run_service_name",
  "operation":"yolo",
  "slice_len":0,
  "body":{
    "model_name":"model_name"

  }
}
```