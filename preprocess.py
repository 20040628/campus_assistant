# 请先安装 openai SDK: pip install openai
from openai import OpenAI
import re
import csv

# 初始化 API 客户端
client = OpenAI(
    api_key="sk-e343c12b259a4a1bb33f5c06cc524c22",
    base_url="https://api.deepseek.com"
)

# 输入文本（可替换为你的院系介绍）
text = '''
请从以下文本中抽取三元组（主语，谓语，宾语），用于构建知识图谱：
材料成型及控制工程专业
课程设置：材料成形理论基础、材料加工工程、模具CAD/CAM
'''

# 调用 DeepSeek-Chat 模型
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个信息抽取专家，擅长从中文文本中提取知识图谱三元组"},
        {"role": "user", "content": text},
    ],
    stream=False
)

# 获取并打印模型输出
output = response.choices[0].message.content
print("模型原始输出：\n", output)

# 正则提取 (实体1, 关系, 实体2) 格式的三元组
triplets = re.findall(r'[(（](.*?),(.*?),(.*?)[)）]', output)

# 输出提取的三元组
print("\n提取到的三元组：")
for triple in triplets:
    print(triple)

# 保存为 CSV 文件
csv_path = "triplets.csv"
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["头实体", "关系", "尾实体"])
    for h, r, t in triplets:
        writer.writerow([h.strip(), r.strip(), t.strip()])

print(f"\n三元组已保存至：{csv_path}")
