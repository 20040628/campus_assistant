import csv


def jaccard_similarity(a, b):
    """基于字符集的 Jaccard 相似度"""
    set_a, set_b = set(a), set(b)
    if not set_a | set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def is_fuzzy_match(triple1, triple2, threshold=0.9):
    """判断两个三元组是否模糊匹配"""
    h1, r1, t1 = triple1
    h2, r2, t2 = triple2
    return (
            jaccard_similarity(h1, h2) >= threshold and
            jaccard_similarity(r1, r2) >= threshold and
            jaccard_similarity(t1, t2) >= threshold
    )


def load_triples(path):
    """读取CSV文件，返回三元组集合"""
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头
        return [tuple(row[:3]) for row in reader if len(row) >= 3]


def evaluate_triples(pred_path, gold_path, match_type="strict", threshold=0.8):
    pred_triples = load_triples(pred_path)
    gold_triples = load_triples(gold_path)

    matched_pred = set()
    matched_gold = set()

    for i, pred in enumerate(pred_triples):
        for j, gold in enumerate(gold_triples):
            match = (
                pred == gold if match_type == "strict"
                else is_fuzzy_match(pred, gold, threshold)
            )
            if match:
                matched_pred.add(i)
                matched_gold.add(j)
                break

    precision = len(matched_pred) / len(pred_triples) if pred_triples else 0.0
    recall = len(matched_gold) / len(gold_triples) if gold_triples else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    print(f"\n🔍 评估模式：{'模糊匹配' if match_type == 'fuzzy' else '严格匹配'}")
    print(f"🔢 预测三元组数: {len(pred_triples)}")
    print(f"✅ 正确预测数: {len(matched_pred)}")
    print(f"📌 标注三元组数: {len(gold_triples)}")
    print(f"\n🎯 Precision: {precision:.2%}")
    print(f"🎯 Recall:    {recall:.2%}")
    print(f"🎯 F1-score:  {f1:.2%}")

    # 可选：打印错误样例
    # false_pos = [pred_triples[i] for i in range(len(pred_triples)) if i not in matched_pred]
    # false_neg = [gold_triples[j] for j in range(len(gold_triples)) if j not in matched_gold]

    # print("\n❌ False Positives (模型预测错误):")
    # for t in false_pos[:5]:
    #     print("  ", t)
    #
    # print("\n❌ False Negatives (漏抽三元组):")
    # for t in false_neg[:5]:
    #     print("  ", t)


# 示例调用
if __name__ == "__main__":
    pred_file = "data/自动抽取/光学与电子信息学院.csv"  # 预测结果文件
    gold_file = "data/人工抽取/光学与电子信息学院.csv"  # 人工标注文件

    # 严格匹配评估
    evaluate_triples(pred_file, gold_file, match_type="strict")

    # 模糊匹配评估（可调阈值）
    evaluate_triples(pred_file, gold_file, match_type="fuzzy", threshold=0.5)
