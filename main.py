import base64
import ollama
import os
import re
from save_info import save_answers_to_json
from system_message import  get_system_message


def initialize_conversation_history():
    """
    初始化对话历史，并添加 System Message
    """
    return [get_system_message()]

def encode_image(image_path):
    """
    读取图片并进行 Base64 编码
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Image file '{image_path}' not found.")
        return None

def clean_response(response_text):
    """
    处理 DeepSeek-R1 的输出，去除 <think> 及相关内容，确保只返回最终答案。
    """
    # 在用deepseek时，删除 <think> 标签及其内容
    response_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)

    return response_text.strip()

def get_answer(model, base64_image, query, conversation_history):
    """
    发送对话请求，并保持对话历史
    """
    if base64_image is None:
        return "Error: No image data available."

    # 添加用户输入到对话历史
    conversation_history.append(
        {
            "role": "user",
            "content": query,
            "images": [base64_image],  # 传入 Base64 编码的图片
        }
    )

    # 发送请求给 `ollama`
    response = ollama.chat(model=model, messages=conversation_history)

    # 解析 AI 响应
    if "message" in response and "content" in response["message"]:
        answer = response["message"]["content"]
    else:
        answer = "Error: Failed to get a response."

    # 记录 AI 的回答
    conversation_history.append({"role": "assistant", "content": answer})

    return answer

def process_images(image_folder, model, questions, output_file):
    """
    处理指定文件夹下的所有图片，并对每张图片进行多轮对话，最后将结果存入 JSON 文件。
    :param image_folder: 图片所在的文件夹路径
    :param model: 处理图片的 AI 模型名称
    :param questions: 需要询问的列表
    :param output_file: 结果存储的 JSON 文件名
    """

    # 确保目录存在
    if not os.path.exists(image_folder):
        print(f"Error: 目录 {image_folder} 不存在！")
        return

    # 获取所有符合格式的图片
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("Error: 未找到任何图片文件！")
        return

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        print(f"Processing image: {image_path}")

        # 读取图片
        base64_image = encode_image(image_path)

        # 初始化对话历史
        conversation_history = initialize_conversation_history()

        for question in questions:
            answer = get_answer(model, base64_image, question, conversation_history)
            final_answer = clean_response(answer)
            print(f"AI: {final_answer}")

            # 保存到 JSON
            save_answers_to_json(final_answer, image_path, output_file)

def main():
    """
    主流程，处理对话逻辑
    """
    # 此处为手工输入部分
    model = "llama3.2-vision"
    image_path = "/media/yx/Elements/Data/jh_data/Night_1/Crossroads_with_trafficlight/result"
    output_file = "try_2.json"

    # 进行多轮对话
    questions = [
        "What is the environmental conditions?",
        "What is the Critical Objects",
        "What is the trajectory?",
    ]

    process_images(image_path, model, questions, output_file)



if __name__ == "__main__":
    main()