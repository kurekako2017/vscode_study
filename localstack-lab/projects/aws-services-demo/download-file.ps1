# Download test-file.txt from LocalStack S3

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Download File from LocalStack S3" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$bucketName = "test-bucket-demo"
$fileName = "test-file.txt"
$localPath = Join-Path (Get-Location) $fileName

# Check if LocalStack is running
Write-Host "[1] Checking LocalStack..." -ForegroundColor Yellow
$running = docker ps --format "{{.Names}}" | Select-String "localstack"
if (-not $running) {
    Write-Host "  ERROR: LocalStack is not running" -ForegroundColor Red
    Write-Host "  Please start LocalStack: docker start localstack" -ForegroundColor Yellow
    exit 1
}
Write-Host "  OK: LocalStack is running" -ForegroundColor Green

# Try to download using AWS CLI
Write-Host "`n[2] Attempting to download file..." -ForegroundColor Yellow
Write-Host "  Bucket: $bucketName" -ForegroundColor White
Write-Host "  File: $fileName" -ForegroundColor White
Write-Host "  Destination: $localPath" -ForegroundColor White

try {
    # Method 1: Using awslocal if available
    $awslocal = Get-Command awslocal -ErrorAction SilentlyContinue
    if ($awslocal) {
        Write-Host "`n  Using awslocal..." -ForegroundColor Gray
        awslocal s3 cp "s3://$bucketName/$fileName" $localPath 2>&1 | Out-Null
    } else {
        # Method 2: Using aws with endpoint
        Write-Host "`n  Using aws cli with endpoint..." -ForegroundColor Gray
        aws --endpoint-url=http://localhost:4566 s3 cp "s3://$bucketName/$fileName" $localPath 2>&1 | Out-Null
    }

    if (Test-Path $localPath) {
        Write-Host "`n  SUCCESS: File downloaded!" -ForegroundColor Green
        Write-Host "`n[3] File content:" -ForegroundColor Yellow
        Write-Host "  ----------------------------------------" -ForegroundColor Cyan
        Get-Content $localPath | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
        Write-Host "  ----------------------------------------" -ForegroundColor Cyan

        Write-Host "`n[4] File information:" -ForegroundColor Yellow
        $fileInfo = Get-Item $localPath
        Write-Host "  Full path: $($fileInfo.FullName)" -ForegroundColor White
        Write-Host "  Size: $($fileInfo.Length) bytes" -ForegroundColor White
        Write-Host "  Created: $($fileInfo.CreationTime)" -ForegroundColor White
    } else {
        throw "File not downloaded"
    }
} catch {
    Write-Host "`n  WARNING: AWS CLI download failed" -ForegroundColor Yellow
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray

    # Method 3: Using Java program to download
    Write-Host "`n  Trying alternative method (Java program)..." -ForegroundColor Yellow

    $javaCode = @"
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import java.io.File;
import java.net.URI;

public class DownloadFile {
    public static void main(String[] args) {
        S3Client s3 = S3Client.builder()
            .endpointOverride(URI.create("http://localhost:4566"))
            .region(Region.US_EAST_1)
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create("test", "test")))
            .forcePathStyle(true)
            .build();

        String content = s3.getObjectAsBytes(
            GetObjectRequest.builder()
                .bucket("$bucketName")
                .key("$fileName")
                .build()
        ).asUtf8String();

        System.out.println(content);
    }
}
"@

    Write-Host "  Run the demo again to create the file:" -ForegroundColor Gray
    Write-Host "  cd D:\dev\study\localstack-lab\projects\aws-services-demo" -ForegroundColor Cyan
    Write-Host "  .\run-demo.ps1" -ForegroundColor Cyan
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "File Location Explanation:" -ForegroundColor Yellow
Write-Host "  - test-file.txt is NOT saved on local disk" -ForegroundColor White
Write-Host "  - It exists in LocalStack container's memory" -ForegroundColor White
Write-Host "  - Storage location: LocalStack S3 simulation" -ForegroundColor White
Write-Host "  - Bucket: $bucketName" -ForegroundColor White
Write-Host "  - Key: $fileName" -ForegroundColor White

if (Test-Path $localPath) {
    Write-Host "`nDownloaded file location:" -ForegroundColor Yellow
    Write-Host "  $(Resolve-Path $localPath)" -ForegroundColor Green
}

Write-Host "`nUseful commands:" -ForegroundColor Cyan
Write-Host "  - List files: aws --endpoint-url=http://localhost:4566 s3 ls s3://$bucketName/" -ForegroundColor Gray
Write-Host "  - View content: aws --endpoint-url=http://localhost:4566 s3 cp s3://$bucketName/$fileName -" -ForegroundColor Gray
Write-Host "  - Download: aws --endpoint-url=http://localhost:4566 s3 cp s3://$bucketName/$fileName ./" -ForegroundColor Gray

Write-Host ""

