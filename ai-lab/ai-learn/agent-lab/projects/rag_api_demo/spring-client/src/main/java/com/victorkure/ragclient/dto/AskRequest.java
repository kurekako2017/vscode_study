package com.victorkure.ragclient.dto;

// 对应 FastAPI /ask 的 JSON 请求体；record 会自动生成构造器和访问方法。
public record AskRequest(
    String question,
    String model
) {
}
