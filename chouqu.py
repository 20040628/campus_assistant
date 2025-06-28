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
    # 用了思维链+少样本学习的prompt
    prompt_v2 = f'''
    你是一个中文信息抽取专家，擅长从文本中抽取用于构建知识图谱的三元组。

    请按照如下步骤思考并输出：
    1. 识别文本中出现的关键实体；
    2. 判断实体之间是否存在关系；
    3. 将抽取的三元组按 (主语, 谓语, 宾语) 格式输出，每条三元组独占一行。
    
    示例：
    一个文件名为公共管理学院的文件中有如下文本：
    公共事业管理专业
    专业实力：公共事业管理是首批国家级一流本科专业建设点、国家级特色专业建设点、湖北省品牌专业，入选湖北省普通本科高校“荆楚卓越人才”协同育人计划。
    培养目标：培养具有公共管理基本理论和专门知识，掌握数字政府、智慧城市的理论和方法，能在党政机关从事政策研究和行政管理，在城市经济管理、市场监管、公共服务、社会治理等领域任职的高级管理人才。
    课程设置：专业核心课程包括公共管理学、微观经济学、宏观经济学、公共政策分析

    输出三元组：
    （公共管理学院, 开设专业, 公共事业管理专业）
    （公共事业管理专业, 属于, 国家级一流本科专业建设点）
    （公共事业管理专业, 属于, 国家级特色专业建设点）
    （公共事业管理专业, 属于, 湖北省品牌专业）
    （公共事业管理专业, 入选, 湖北省普通本科高校“荆楚卓越人才”协同育人计划。）
    （公共事业管理专业, 开设课程, 公共管理学）
    （公共事业管理专业, 开设课程, 微观经济学）
    （公共事业管理专业, 开设课程, 宏观经济学）
    （公共事业管理专业, 开设课程, 公共政策分析）
    
    现在请处理以下文本：
    {content}
    '''

    # 调用 DeepSeek 模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个信息抽取专家，擅长从中文文本中提取知识图谱三元组"},
            {"role": "user", "content": prompt_v2},
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
csv_filename = "improved_result.csv"
with open(csv_filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["头实体", "关系", "尾实体", "来源文件"])
    writer.writerows(all_triplets)

print(f"全部三元组已保存到文件：{csv_filename}")
