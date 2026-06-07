"""最小可部署服务 demo。

这个脚本用 Python 标准库启动一个 HTTP 服务，
用于演示：
- 服务入口
- 环境变量
- 容器化
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# 监听所有网卡，方便容器里访问。
HOST = "0.0.0.0"
# 这个 demo 默认使用 8088 端口。
PORT = 8088


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        # 组装一个简单的健康检查响应。
        payload = {
            "name": os.getenv("APP_NAME", "agent-advanced-container-demo"),
            "status": "ok",
            "message": "This is a tiny deployable service demo.",
        }
        # 转成 JSON 字节串。
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        # 返回 200 状态码。
        self.send_response(200)
        # 告诉客户端响应内容是 JSON。
        self.send_header("Content-Type", "application/json; charset=utf-8")
        # 说明 body 的长度。
        self.send_header("Content-Length", str(len(body)))
        # 结束响应头。
        self.end_headers()
        # 写出响应体。
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # 这里故意不打印访问日志，避免示例输出太吵。
        return


def main() -> None:
    # 创建 HTTPServer 实例。
    server = HTTPServer((HOST, PORT), Handler)
    # 打印启动信息。
    print(f"Serving on http://{HOST}:{PORT}")
    # 一直运行，直到进程退出。
    server.serve_forever()


if __name__ == "__main__":
    main()
