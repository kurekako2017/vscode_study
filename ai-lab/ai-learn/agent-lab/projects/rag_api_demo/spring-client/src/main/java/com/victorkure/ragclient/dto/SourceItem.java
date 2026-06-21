package com.victorkure.ragclient.dto;

// 一条 RAG 引用来源：标签用于定位文档，score 表示关键词匹配分数。
public record SourceItem(
    String sourceLabel,
    int score
) {
}
