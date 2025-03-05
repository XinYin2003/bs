# dict1=        {
#             "image": "1.jpeg"
#         }
# dict2=        {
#             "Weather": "Rainy",
#             "Time": "Day",
#             "Road Environment": "Urban",
#             "Lane Options":
#             [
#                 "Own Lane",
#                 "Right Lane"
#             ],
#             "Ego Lane Position": "Middle Lane"
#         }
# dict1.update(dict2)
# print(dict1)

import json

ai_output = 'AI: The trajectory is: {"Reason": "heavy rain, night time in an urban area with multiple critical objects ahead.", "Meta Action": ["slow down","change lane to the right"]}'

# 解决方案：提取 JSON 部分
json_start = ai_output.find("{")
if json_start != -1:
    json_string = ai_output[json_start:]  # 获取 `{` 之后的内容
    try:
        parsed_json = json.loads(json_string)  # 解析 JSON
        print(parsed_json)
    except json.JSONDecodeError as e:
        print("JSON 解析错误:", e)
else:
    print("未找到 JSON 数据")

