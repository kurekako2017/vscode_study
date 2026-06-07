package com.victorkure.ragclient.dto;

public record AskRequest(
    String question,
    String model
) {
}
