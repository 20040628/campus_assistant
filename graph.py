import csv
from py2neo import Graph, Node, Relationship

# 连接 Neo4j # neo4j.bat console （命令行启动neo4j）
graph = Graph("http://localhost:7474", auth=("neo4j", "Wjq!040628"), name="neo4j")

# 清空数据库
graph.delete_all()


# 从 CSV 读取三元组数据
def read_triplets(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        return [row[:3] for row in reader if len(row) >= 3]


# 构建三元组知识图谱
def create_triplet_graph(triplets):
    for head, relation, tail in triplets:
        # 去除空格，标准化
        head = head.strip()
        relation = relation.strip()
        tail = tail.strip()

        # 获取或创建头实体
        head_node = graph.nodes.match("实体", name=head).first()
        if not head_node:
            head_node = Node("实体", name=head)
            graph.create(head_node)

        # 获取或创建尾实体
        tail_node = graph.nodes.match("实体", name=tail).first()
        if not tail_node:
            tail_node = Node("实体", name=tail)
            graph.create(tail_node)

        # 检查是否已有相同的关系存在
        existing_rel = graph.relationships.match((head_node, tail_node), r_type=relation).first()
        if not existing_rel:
            rel = Relationship(head_node, relation, tail_node)
            graph.create(rel)


if __name__ == '__main__':
    triplet_file = 'final_triples.csv'
    data = read_triplets(triplet_file)
    create_triplet_graph(data)