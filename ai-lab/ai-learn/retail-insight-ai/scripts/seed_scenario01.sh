#!/usr/bin/env bash
# Scenario01 业务样例种子脚本（PostgreSQL-only / 幂等 / 零 Provider 调用）
#
# 用途：通过真实 login / documents / import / chunk API 导入 Scenario01 文档。
# 禁止：Retrieval、AI 分析、报告、审批、真实 LLM、删除现有数据。
# 不随 Compose 自动启动；需人工执行。
#
# 用法（项目根）：
#   ./scripts/seed_scenario01.sh
#   BASE_URL=http://127.0.0.1:8000 ./scripts/seed_scenario01.sh
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
USERNAME="${SEED_USERNAME:-admin}"
PASSWORD="${SEED_PASSWORD:-Admin#2026!}"
SAMPLE_DIR="${ROOT_DIR}/docs/learning/sample-data/Scenario01_Sales_Decline"

# 业务文档 01-06（07-10 为问题/输入例/测试说明，不入库为检索语料）
mapfile -t SEED_FILES < <(ls -1 "${SAMPLE_DIR}"/0{1,2,3,4,5,6}_*.md 2>/dev/null || true)

if [[ ${#SEED_FILES[@]} -eq 0 ]]; then
  echo "ERROR: Scenario01 业务文档未找到: ${SAMPLE_DIR}" >&2
  exit 1
fi

json_field() {
  # 最小 JSON 字段提取（无依赖 jq）；字段必须为字符串或数字。
  local json="$1"
  local key="$2"
  python3 - "$json" "$key" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
key = sys.argv[2]
def dig(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur
val = dig(data, key)
if val is None:
    print("")
else:
    print(val)
PY
}

echo "=== Scenario01 Seed (PostgreSQL-only) ==="
echo "BASE_URL=${BASE_URL}"
echo "sample_dir=${SAMPLE_DIR}"
echo "provider_call_target=0"

# 1) 后端健康与 backend 类型
HEALTH_JSON="$(curl -fsS "${BASE_URL}/health" || true)"
if [[ -z "${HEALTH_JSON}" ]]; then
  echo "ERROR: Backend 不可达: ${BASE_URL}/health" >&2
  exit 1
fi
BACKEND="$(json_field "${HEALTH_JSON}" "repository_backend")"
if [[ -z "${BACKEND}" ]]; then
  BACKEND="$(json_field "${HEALTH_JSON}" "data.repository_backend")"
fi
if [[ "${BACKEND}" != "postgres" ]]; then
  echo "ERROR: 只允许 PostgreSQL。当前 repository_backend=${BACKEND:-unknown}（InMemory 立即拒绝）" >&2
  exit 2
fi
echo "repository_backend=postgres OK"

# 2) Login
LOGIN_JSON="$(curl -fsS -X POST "${BASE_URL}/api/v1/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(json_field "${LOGIN_JSON}" "data.access_token")"
if [[ -z "${TOKEN}" ]]; then
  TOKEN="$(json_field "${LOGIN_JSON}" "access_token")"
fi
if [[ -z "${TOKEN}" ]]; then
  echo "ERROR: login 失败（不打印响应正文）" >&2
  exit 3
fi
AUTH="Authorization: Bearer ${TOKEN}"
echo "login=OK user=${USERNAME}"

# 3) 现有文档 title → document_id 映射（幂等；纯 Python 解析，避免 shell 对日文 title 匹配失败）
LOOKUP_JSON="$(curl -fsS "${BASE_URL}/api/v1/documents?include_archived=true&limit=100" -H "${AUTH}")"
# 输出 JSON 对象 {title: {document_id,status,chunk_count}}
EXISTING_JSON="$(python3 - "${LOOKUP_JSON}" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
data = payload.get("data") or payload if isinstance(payload, dict) else {}
items = data.get("items") or []
out = {}
for item in items:
    title = item.get("title") or ""
    if not title:
        continue
    out[title] = {
        "document_id": item.get("document_id") or "",
        "status": item.get("status") or "",
        "chunk_count": item.get("chunk_count") if item.get("chunk_count") is not None else 0,
        "searchable": bool(item.get("searchable")),
    }
print(json.dumps(out, ensure_ascii=False))
PY
)"

provider_calls=0
created=0
reused=0
results=()

for filepath in "${SEED_FILES[@]}"; do
  filename="$(basename "${filepath}")"
  title="${filename%.md}"
  # 推荐问题来自文件名关联（不读取全文到 stdout）
  recommended=""
  case "${filename}" in
    01_*) recommended="関東地区の飲料売上が 2026年6月に落ちた主因は何か" ;;
    02_*) recommended="神奈川で夕方欠品が増加した理由は何ですか" ;;
    03_*) recommended="販促キャンペーンの効果は売上低下とどう関係しますか" ;;
    04_*) recommended="顧客アンケートで最頻の不満は何ですか" ;;
    05_*) recommended="競合店舗の値下げはどの地域で最も強いか" ;;
    06_*) recommended="KPI月次報告でどの指標が悪化しましたか" ;;
    *) recommended="関東飲料売上下降の主要因は何か" ;;
  esac

  document_id="$(python3 - "${EXISTING_JSON}" "${title}" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
title = sys.argv[2]
row = data.get(title) or {}
print(row.get("document_id") or "")
PY
)"
  status="$(python3 - "${EXISTING_JSON}" "${title}" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
title = sys.argv[2]
row = data.get(title) or {}
print(row.get("status") or "")
PY
)"
  chunk_count="$(python3 - "${EXISTING_JSON}" "${title}" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
title = sys.argv[2]
row = data.get(title) or {}
print(row.get("chunk_count") if row.get("chunk_count") is not None else 0)
PY
)"

  if [[ -n "${document_id}" ]]; then
    reused=$((reused + 1))
    echo "reuse title=${title} document_id=${document_id} status=${status}"
  else
    # Upload（multipart）；Idempotency-Key 基于文件名稳定
    idem="scenario01-$(printf '%s' "${filename}" | tr -c 'A-Za-z0-9._-' '-')"
    metadata="$(python3 -c 'import json,sys; print(json.dumps({"title":sys.argv[1],"description":"Scenario01 seed","owner":"scenario01-seed","tags":["scenario01","seed"],"language":"ja"}, ensure_ascii=False))' "${title}")"
    # 上传前已有 document_id 集合（用于识别 checksum/Idempotency 重放）
    known_ids="$(python3 - "${EXISTING_JSON}" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
print(" ".join(sorted({v.get("document_id") for v in data.values() if v.get("document_id")})))
PY
)"
    UPLOAD_JSON="$(curl -fsS -X POST "${BASE_URL}/api/v1/documents" \
      -H "${AUTH}" \
      -H "Idempotency-Key: ${idem}" \
      -F "file=@${filepath};type=text/markdown" \
      -F "metadata=${metadata}")"
    document_id="$(json_field "${UPLOAD_JSON}" "data.document_id")"
    if [[ " ${known_ids} " == *" ${document_id} "* ]]; then
      # 服务端按 Idempotency-Key / checksum 返回了已有文档 → 不新增
      reused=$((reused + 1))
      echo "reuse(idempotent-upload) title=${title} document_id=${document_id}"
    else
      status="uploaded"
      created=$((created + 1))
      echo "upload title=${title} document_id=${document_id}"
    fi
  fi

  if [[ -z "${document_id}" ]]; then
    echo "ERROR: missing document_id for ${title}" >&2
    exit 4
  fi

  # 统一以 document detail 为事实源（避免 upload session status=completed 误导）
  DETAIL_JSON="$(curl -fsS "${BASE_URL}/api/v1/documents/${document_id}" -H "${AUTH}" || true)"
  if [[ -n "${DETAIL_JSON}" ]]; then
    status="$(json_field "${DETAIL_JSON}" "data.status")"
    if [[ -z "${status}" ]]; then status="$(json_field "${DETAIL_JSON}" "status")"; fi
    cc="$(json_field "${DETAIL_JSON}" "data.chunk_count")"
    if [[ -n "${cc}" ]]; then chunk_count="${cc}"; fi
  fi
  CHUNKS_JSON="$(curl -fsS "${BASE_URL}/api/v1/documents/${document_id}/chunks" -H "${AUTH}" || true)"
  if [[ -n "${CHUNKS_JSON}" ]]; then
    chunk_count="$(python3 - "${CHUNKS_JSON}" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
data = payload.get("data") or payload
items = data.get("items") or []
print(len(items))
PY
)"
  fi

  # Import（幂等：validated/indexed 可跳过；失败不删除）
  if [[ "${status}" == "uploaded" || "${status}" == "failed" || -z "${status}" ]]; then
    IMPORT_JSON="$(curl -fsS -X POST "${BASE_URL}/api/v1/documents/${document_id}/import" -H "${AUTH}" || true)"
    if [[ -n "${IMPORT_JSON}" ]]; then
      status="validated"
      echo "import document_id=${document_id} status=validated"
    fi
  fi

  # Chunk（若 chunk_count 已 >0 则跳过；replace 幂等）
  if [[ -z "${chunk_count}" || "${chunk_count}" == "0" || "${chunk_count}" == "None" ]]; then
    CHUNK_JSON="$(curl -fsS -X POST "${BASE_URL}/api/v1/documents/${document_id}/chunks" -H "${AUTH}" || true)"
    if [[ -n "${CHUNK_JSON}" ]]; then
      chunk_count="$(python3 - "${CHUNK_JSON}" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
data = payload.get("data") or payload
items = data.get("items") or []
print(len(items))
PY
)"
      status="validated"
      echo "chunk document_id=${document_id} chunk_count=${chunk_count}"
    fi
  fi

  # 最终刷新 status/chunk_count（不输出正文）
  DETAIL_JSON="$(curl -fsS "${BASE_URL}/api/v1/documents/${document_id}" -H "${AUTH}" || true)"
  if [[ -n "${DETAIL_JSON}" ]]; then
    status="$(json_field "${DETAIL_JSON}" "data.status")"
    if [[ -z "${status}" ]]; then status="$(json_field "${DETAIL_JSON}" "status")"; fi
    cc="$(json_field "${DETAIL_JSON}" "data.chunk_count")"
    if [[ -n "${cc}" ]]; then chunk_count="${cc}"; fi
  fi
  CHUNKS_JSON="$(curl -fsS "${BASE_URL}/api/v1/documents/${document_id}/chunks" -H "${AUTH}" || true)"
  if [[ -n "${CHUNKS_JSON}" ]]; then
    chunk_count="$(python3 - "${CHUNKS_JSON}" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
data = payload.get("data") or payload
items = data.get("items") or []
print(len(items))
PY
)"
  fi

  results+=("document_id=${document_id} status=${status} chunk_count=${chunk_count} recommended_question=${recommended}")
done

echo "=== Seed summary ==="
echo "created=${created} reused=${reused} provider_calls=${provider_calls}"
for line in "${results[@]}"; do
  echo "${line}"
done
echo "OK Scenario01 seed complete (no retrieval / no AI / no approval)"
