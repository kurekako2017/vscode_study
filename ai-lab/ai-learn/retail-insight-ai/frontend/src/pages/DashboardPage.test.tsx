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
    expect(screen.getAllByText(/PostgreSQL/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/InMemory/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/静态/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/默认关闭/).length).toBeGreaterThan(0);
  });

  it("shows feature entry cards", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getByRole("button", { name: "打开 KPI任务分析" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "文書管理を開く" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "打开 RAG/AI分析" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "打开承認管理" })).toBeInTheDocument();
  });

  it("shows the enterprise business flow and end-to-end learning case", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getByRole("heading", { name: "企业业务流程" })).toBeInTheDocument();
    expect(screen.getByText("ERIP-E2E-001")).toBeInTheDocument();
    expect(screen.getByText("当前未连接：前端没有单独的最终审计报告汇总页面。")).toBeInTheDocument();
  });

  it("sends navigation target when shortcut buttons are clicked", () => {
    const onNavigate = vi.fn();
    render(<DashboardPage onNavigate={onNavigate} />);

    fireEvent.click(screen.getByRole("button", { name: "打开 KPI任务分析" }));
    fireEvent.click(screen.getByRole("button", { name: "文書管理を開く" }));
    fireEvent.click(screen.getByRole("button", { name: "打开 RAG/AI分析" }));
    fireEvent.click(screen.getByRole("button", { name: "打开承認管理" }));

    expect(onNavigate).toHaveBeenNthCalledWith(1, "analysis");
    expect(onNavigate).toHaveBeenNthCalledWith(2, "documents");
    expect(onNavigate).toHaveBeenNthCalledWith(3, "rag");
    expect(onNavigate).toHaveBeenNthCalledWith(4, "approval");
  });

  it("renders capability boundary without crashing in compact layout", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getAllByText("正式入口").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Docker http://127.0.0.1:8080").length).toBeGreaterThan(0);
    expect(screen.getAllByText("默认关闭").length).toBeGreaterThan(0);
  });
});
