from __future__ import annotations

import numpy as np

from _compat import hash_embed, cosine_similarity


def _encode(text: str):
    return hash_embed(text, 384)[None, :]


text_emb = _encode("datawhale开源组织的logo")
img_emb_1 = _encode("datawhale01.png")
multi_emb_1 = _encode("datawhale01.png datawhale开源组织的logo")
img_emb_2 = _encode("datawhale02.png")
multi_emb_2 = _encode("datawhale02.png datawhale开源组织的logo")

sim_1 = cosine_similarity(img_emb_1[0], img_emb_2)[0][0]
sim_2 = cosine_similarity(img_emb_1[0], multi_emb_1)[0][0]
sim_3 = cosine_similarity(text_emb[0], multi_emb_1)[0][0]
sim_4 = cosine_similarity(multi_emb_1[0], multi_emb_2)[0][0]

print("=== 相似度计算结果 ===")
print(f"纯图像 vs 纯图像: {sim_1:.4f}")
print(f"图文结合1 vs 纯图像: {sim_2:.4f}")
print(f"图文结合1 vs 纯文本: {sim_3:.4f}")
print(f"图文结合1 vs 图文结合2: {sim_4:.4f}")

print("\n=== 嵌入向量信息 ===")
print(f"多模态向量维度: {multi_emb_1.shape}")
print(f"图像向量维度: {img_emb_1.shape}")
print(f"多模态向量示例 (前10个元素): {multi_emb_1[0][:10]}")
print(f"图像向量示例 (前10个元素):   {img_emb_1[0][:10]}")
