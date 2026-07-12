import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { DashboardPage } from "./DashboardPage";

describe("DashboardPage", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders overview and runtime facts by default", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getByRole("heading", { name: "Enterprise Retail Intelligence Platform" })).toBeInTheDocument();
    expect(screen.getByText("InMemory")).toBeInTheDocument();
    expect(screen.getByText("静态数据")).toBeInTheDocument();
    expect(screen.getAllByText("未启用").length).toBeGreaterThan(0);
  });

  it("shows feature entry cards", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getByRole("button", { name: "分析依頼を開く" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "文書管理を開く" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "RAG検索を開く" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "承認管理を開く" })).toBeInTheDocument();
  });

  it("sends navigation target when shortcut buttons are clicked", () => {
    const onNavigate = vi.fn();
    render(<DashboardPage onNavigate={onNavigate} />);

    fireEvent.click(screen.getByRole("button", { name: "分析依頼を開く" }));
    fireEvent.click(screen.getByRole("button", { name: "文書管理を開く" }));
    fireEvent.click(screen.getByRole("button", { name: "RAG検索を開く" }));
    fireEvent.click(screen.getByRole("button", { name: "承認管理を開く" }));

    expect(onNavigate).toHaveBeenNthCalledWith(1, "analysis");
    expect(onNavigate).toHaveBeenNthCalledWith(2, "documents");
    expect(onNavigate).toHaveBeenNthCalledWith(3, "rag");
    expect(onNavigate).toHaveBeenNthCalledWith(4, "approval");
  });

  it("renders capability boundary without crashing in compact layout", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getAllByText("关键词检索").length).toBeGreaterThan(0);
    expect(screen.getAllByText("未连接").length).toBeGreaterThan(0);
    expect(screen.getAllByText("尚未可用").length).toBeGreaterThan(0);
  });
});
