param(
    [string]$Provider = "openai",
    [string]$Prompt = "请用中文写一个排序算法示例",
    [switch]$DryRun
)

$provider = $Provider.ToLower()
$envMap = @{ openai = 'OPENAI_API_KEY'; claude = 'CLAUDE_API_KEY'; gemini = 'GEMINI_API_KEY' }
$envName = $envMap[$provider]

switch ($provider) {
    'openai' {
        $bodyJson = @"
{"model":"gpt-4o-mini","messages":[{"role":"user","content":"$Prompt"}]}
"@
    }
    'claude' {
        $bodyJson = @"
{"model":"claude-2.1","prompt":"$Prompt","max_tokens":800}
"@
    }
    'gemini' {
        $bodyJson = @"
{"prompt":{"text":"$Prompt"},"temperature":0.2}
"@
    }
    default {
        Write-Error "不支持的 Provider: $Provider"
        exit 1
    }
}

if ($DryRun) {
    Write-Host "[DryRun] Provider: $Provider" -ForegroundColor Cyan
    Write-Host "[DryRun] 请求体：" -ForegroundColor Cyan
    Write-Host $bodyJson
    exit 0
}

$apiKey = [Environment]::GetEnvironmentVariable($envName, 'User')
if (-not $apiKey) { $apiKey = [Environment]::GetEnvironmentVariable($envName, 'Process') }
if (-not $apiKey) { Write-Error "环境变量 $envName 未设置。请先设置 API Key 后重试。"; exit 1 }

try {
    if ($provider -eq 'openai') {
        $uri = 'https://api.openai.com/v1/chat/completions'
        $headers = @{ Authorization = "Bearer $apiKey" }
        $resp = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -ContentType 'application/json' -Body $bodyJson
        $resp.choices | ForEach-Object { $_.message.content }
    } elseif ($provider -eq 'claude') {
        $uri = 'https://api.anthropic.com/v1/complete'
        $headers = @{ 'x-api-key' = $apiKey; 'Content-Type' = 'application/json' }
        $resp = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $bodyJson
        $resp
    } elseif ($provider -eq 'gemini') {
        $gk = $apiKey
        $uri = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate?key=$gk"
        $resp = Invoke-RestMethod -Uri $uri -Method Post -ContentType 'application/json' -Body $bodyJson
        $resp
    }
} catch {
    Write-Error "请求失败：$($_.Exception.Message)"
    exit 1
}