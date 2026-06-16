// App 是整个页面的总控组件：
// 1. 拉健康检查
// 2. 管理当前输入框和对话 turns
// 3. 把 useDeepAgentSession 返回的状态拼到界面上
import {
  ApiOutlined,
  BranchesOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  CloudServerOutlined,
  DatabaseOutlined,
  FileSearchOutlined,
  ToolOutlined
} from "@ant-design/icons";
import { Alert, App as AntApp, Button } from "antd";
import { useEffect, useRef, useState } from "react";
import { ChatComposer } from "./components/ChatComposer";
import { ConversationThread } from "./components/ConversationThread";
import type { ChatTurn } from "./components/ConversationThread";
import { getHealthStatus } from "./lib/api";
import { API_BASE_URL, WS_BASE_URL } from "./lib/config";
import { useDeepAgentSession } from "./hooks/useDeepAgentSession";
import type { ConnectionState, HealthResponse, UploadedItem } from "./types";

function connectionLabel(state: ConnectionState): string {
  const labels: Record<ConnectionState, string> = {
    connecting: "连接中",
    connected: "已连接",
    reconnecting: "重连中",
    closed: "已关闭"
  };
  return labels[state];
}

function createTurn(content: string): ChatTurn {
  // 每次用户点击发送时，前端会先创建一个“占位中的对话轮次”，
  // 等后端事件回来后，再把这个 turn 填完整。
  return {
    id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}`,
    content,
    events: [],
    files: [],
    isRunning: true,
    result: "",
    timestamp: new Date().toISOString()
  };
}

export default function App() {
  const { message } = AntApp.useApp();
  const [query, setQuery] = useState("");
  const [stagedItems, setStagedItems] = useState<UploadedItem[]>([]);
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState("");
  const streamRef = useRef<HTMLElement | null>(null);
  const session = useDeepAgentSession();

  useEffect(() => {
    // 页面刚打开时先打一次健康检查，
    // 让用户立刻看到 Backend / LLM / MySQL 是否可用。
    let cancelled = false;

    getHealthStatus()
      .then((response) => {
        if (!cancelled) {
          setHealth(response);
          setHealthError("");
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setHealthError(error instanceof Error ? error.message : "健康检查失败");
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    // turns 的最后一项始终代表“当前正在执行的那轮对话”。
    // 所以后端新推来的 events/result/files 只需要覆盖最后一条即可。
    setTurns((previous) => {
      if (previous.length === 0) {
        return previous;
      }

      const latestTurn = previous[previous.length - 1];
      const nextLatestTurn = {
        ...latestTurn,
        events: session.events,
        files: session.files,
        isRunning: session.isRunning,
        result: session.result
      };

      return [...previous.slice(0, -1), nextLatestTurn];
    });
  }, [session.events, session.files, session.isRunning, session.result]);

  useEffect(() => {
    // 每次 turns 变化后，把对话区域滚动到底部，
    // 这样用户能直接看到最新事件和结果。
    const streamNode = streamRef.current;
    if (!streamNode) {
      return;
    }

    window.requestAnimationFrame(() => {
      streamNode.scrollTo({
        top: streamNode.scrollHeight,
        behavior: "smooth"
      });
    });
  }, [turns]);

  async function handleSubmit() {
    // 发送任务的顺序：
    // 1. 先做前端输入校验
    // 2. 先把用户消息插入对话区
    // 3. 再真正请求后端启动任务
    const cleanQuery = query.trim();
    if (!cleanQuery) {
      message.warning("请输入研搜任务");
      return;
    }

    const nextTurn = createTurn(cleanQuery);
    setTurns((previous) => [...previous, nextTurn]);
    setQuery("");

    try {
      await session.submitTask(cleanQuery);
      message.success("任务已启动，执行过程会显示在对话中");
    } catch (error) {
      setTurns((previous) =>
        previous.map((turn) =>
          turn.id === nextTurn.id
            ? {
                ...turn,
                isRunning: false,
                result: error instanceof Error ? error.message : "任务启动失败"
              }
            : turn
        )
      );
      message.error(error instanceof Error ? error.message : "任务启动失败");
    }
  }

  async function handleCancel() {
    try {
      const response = await session.cancelCurrentTask();
      message.info(response.status === "cancelling" ? "取消请求已发送，正在等待当前调用结束" : "任务已取消");
    } catch (error) {
      message.error(error instanceof Error ? error.message : "取消任务失败");
    }
  }

  async function handleUpload(items: UploadedItem[]) {
    try {
      const response = await session.uploadFiles(items);
      setStagedItems([]);
      message.success(`已上传 ${response.files.length} 个文件`);
    } catch (error) {
      message.error(error instanceof Error ? error.message : "上传失败");
    }
  }

  function handleNewSession() {
    // 新会话不只是清空输入框，还要重置 thread_id 和会话状态。
    session.resetSession();
    setTurns([]);
    setQuery("");
    setStagedItems([]);
  }

  const online = session.connectionState === "connected";

  return (
    <div className="chat-app-shell min-h-dvh">
      <aside className="chat-sidebar" aria-label="会话信息">
        <div className="sidebar-brand">
          <span className="panel-kicker">DEEPSEARCH</span>
          <h1>深度研搜</h1>
          <p>对话式多智能体研究台</p>
        </div>

        <Button className="new-chat-button" block onClick={handleNewSession}>
          新建研搜
        </Button>

        <div className="sidebar-section">
          <span className="sidebar-label">THREAD</span>
          <strong className="thread-id" title={session.threadId}>
            {session.threadId.slice(0, 8)}
          </strong>
        </div>

        <div className="sidebar-status-list">
          <div className={`sidebar-status ${online ? "sidebar-status--online" : "sidebar-status--warn"}`}>
            <ApiOutlined aria-hidden />
            <span>WebSocket</span>
            <strong>{connectionLabel(session.connectionState)}</strong>
          </div>
          <div className="sidebar-status">
            <BranchesOutlined aria-hidden />
            <span>助手调度</span>
            <strong>{session.stats.assistantEvents}</strong>
          </div>
          <div className="sidebar-status">
            <ToolOutlined aria-hidden />
            <span>工具调用</span>
            <strong>{session.stats.toolEvents}</strong>
          </div>
          <div className={session.stats.errorEvents > 0 ? "sidebar-status sidebar-status--error" : "sidebar-status"}>
            <CloseCircleOutlined aria-hidden />
            <span>异常</span>
            <strong>{session.stats.errorEvents}</strong>
          </div>
        </div>

        <div className="sidebar-section">
          <span className="sidebar-label">AGENTS</span>
          <ul className="agent-mini-list">
            <li>
              <CloudServerOutlined aria-hidden />
              网络搜索助手
            </li>
            <li>
              <DatabaseOutlined aria-hidden />
              数据库查询助手
            </li>
            <li>
              <FileSearchOutlined aria-hidden />
              本地知识库助手
            </li>
          </ul>
        </div>

        <div className="sidebar-section sidebar-endpoints">
          <span className="sidebar-label">ENDPOINTS</span>
          <code>{API_BASE_URL}</code>
          <code>{WS_BASE_URL}</code>
        </div>

        <div className="sidebar-section sidebar-health">
          <span className="sidebar-label">HEALTH</span>
          {health ? (
            <>
              <div className={`sidebar-health-row ${health.backend === "alive" ? "sidebar-health-row--ok" : ""}`}>
                <strong>Backend</strong>
                <span>{health.backend}</span>
              </div>
              <div className="sidebar-health-row">
                <strong>LLM</strong>
                <span>
                  {health.llm.configured
                    ? `${health.llm.provider} · ${health.llm.source} / ${health.llm.model}`
                    : "未配置"}
                </span>
              </div>
              <div className="sidebar-health-row">
                <strong>MySQL</strong>
                <span>{health.mysql.configured ? `${health.mysql.host}:${health.mysql.port}` : "未配置"}</span>
              </div>
              <div className="sidebar-health-row">
                <strong>Services</strong>
                <span>
                  Tavily {health.services.tavily ? "OK" : "OFF"} · 本地知识库{" "}
                  {health.services.local_knowledge_base ? "OK" : "OFF"}
                </span>
              </div>
            </>
          ) : (
            <div className="sidebar-health-row sidebar-health-row--muted">
              <strong>检查</strong>
              <span>{healthError || "正在读取后端状态..."}</span>
            </div>
          )}
        </div>
      </aside>

      <main className="chat-main">
        <header className="chat-topbar">
          <div>
            <span className="panel-kicker">CHAT WORKSPACE</span>
            <h2>深度研搜对话</h2>
          </div>
          <div className={`run-indicator ${session.isRunning ? "run-indicator--live" : ""}`}>
            {session.isRunning ? <BranchesOutlined aria-hidden /> : <CheckCircleOutlined aria-hidden />}
            {session.isRunning ? "研搜中" : "待命"}
          </div>
        </header>

        {session.lastError ? (
          <Alert
            className="chat-alert"
            message={session.lastError}
            showIcon
            type="error"
          />
        ) : null}

        <section className="chat-stream-panel" ref={streamRef}>
          <ConversationThread
            onUseExample={setQuery}
            turns={turns}
          />
        </section>

        <ChatComposer
          isCancelling={session.isCancelling}
          isRunning={session.isRunning}
          isUploading={session.isUploading}
          onCancel={handleCancel}
          onNewSession={handleNewSession}
          onQueryChange={setQuery}
          onStagedItemsChange={setStagedItems}
          onSubmit={handleSubmit}
          onUpload={handleUpload}
          query={query}
          stagedItems={stagedItems}
          uploadedItems={session.uploadedItems}
        />
      </main>
    </div>
  );
}
