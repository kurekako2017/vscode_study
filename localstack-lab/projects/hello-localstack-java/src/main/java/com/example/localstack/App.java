package com.example.localstack;

import java.net.URI;
import java.time.Instant;
import java.time.format.DateTimeFormatter;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.S3Configuration;
import software.amazon.awssdk.core.ResponseBytes;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.core.sync.ResponseTransformer;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.S3Exception;

public class App {
    public static void main(String[] args) {
        String endpoint = System.getenv().getOrDefault("LOCALSTACK_ENDPOINT_URL", "http://s3.localhost.localstack.cloud:4566");
        String bucket = "hello-localstack-java";
        String key = "hello.txt";
        String body = "Hello LocalStack from Java! UTC now: " + DateTimeFormatter.ISO_INSTANT.format(Instant.now()) + "\n";

        S3Client s3 = S3Client.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.US_EAST_1)
            // LocalStack 走 localhost:4566 需要 path-style，否则虚拟域名解析会失败
            .serviceConfiguration(S3Configuration.builder().pathStyleAccessEnabled(true).build())
            .credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test")))
            .build();

        try {
                // S3 us-east-1 不需要设置 LocationConstraint；LocalStack 亦同，直接创建桶即可
                s3.createBucket(CreateBucketRequest.builder()
                    .bucket(bucket)
                    .build());
        } catch (S3Exception e) {
            if (!"BucketAlreadyOwnedByYou".equals(e.awsErrorDetails().errorCode())) {
                throw e;
            }
        }

        s3.putObject(
                PutObjectRequest.builder().bucket(bucket).key(key).build(),
                RequestBody.fromString(body)
        );

        ResponseBytes<GetObjectResponse> response = s3.getObject(
            GetObjectRequest.builder().bucket(bucket).key(key).build(),
            ResponseTransformer.toBytes());

        System.out.println("Endpoint: " + endpoint);
        System.out.println("Bucket: " + bucket);
        System.out.println("Key: " + key);
        System.out.println("Content:\n" + response.asUtf8String());
    }
}
