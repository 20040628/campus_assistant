# 请先安装 openai: pip install openai
from openai import OpenAI
import re
import csv
import os

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key="",
    base_url="https://api.deepseek.com"
)

# 设置文件夹路径（确保路径中没有错别字）
folder_path = "./data/本科院系设置"

# 获取该文件夹下所有 .txt 文件
txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

# 初始化所有三元组列表
all_triplets = []

for txt_file in txt_files:
    file_path = os.path.join(folder_path, txt_file)
    print(f"\n正在处理文件：{file_path}")

    # 读取文本内容
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 构造 prompt
    prompt = f'''请从以下文本中抽取三元组（主语，谓语，宾语），用于构建知识图谱：{content}'''

    # 调用 DeepSeek 模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个信息抽取专家，擅长从中文文本中提取知识图谱三元组"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    # 获取输出内容
    output = response.choices[0].message.content
    print("模型输出：")
    print(output)

    # 正则提取三元组 (头, 关系, 尾)
    triplets = re.findall(r'[（(](.*?)[,，](.*?)[,，](.*?)[)）]', output)

    # 添加文件来源标签并存储
    for h, r, t in triplets:
        all_triplets.append([h.strip(), r.strip(), t.strip(), txt_file])

# 写入所有结果到一个 CSV 文件
csv_filename = "all_triplets.csv"
with open(csv_filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["头实体", "关系", "尾实体", "来源文件"])
    writer.writerows(all_triplets)

print(f"全部三元组已保存到文件：{csv_filename}")
