import json
import os


def save_answers_to_json(answer_str, filename):
    """
    将 AI 返回的 JSON 字符串解析，并追加到 JSON 文件中。

    :param answer_str: AI 返回的 JSON 字符串
    :param filename: JSON 文件名（默认 "ai_response.json"）
    """
    try:
        # 解析传入的 JSON 字符串
        new_data = json.loads(answer_str.strip())  # 解析 JSON

        # 如果文件已存在，则读取现有数据
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)  # 读取已有 JSON
                except json.JSONDecodeError:
                    existing_data = {}  # 文件损坏或为空，则初始化为空字典
        else:
            existing_data = {}  # 如果文件不存在，则初始化为空字典

        # 追加新数据到现有 JSON
        if "responses" not in existing_data:
            existing_data["responses"] = []  # 确保有一个 "responses" 列表存储多个 AI 响应

        existing_data["responses"].append(new_data)  # 追加新数据

        # 写回 JSON 文件
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

        print(f"AI response has been appended to '{filename}'")

    except json.JSONDecodeError as e:
        print(f"Error: The provided string is not valid JSON.\nContent: {answer_str}\nError: {e}")

