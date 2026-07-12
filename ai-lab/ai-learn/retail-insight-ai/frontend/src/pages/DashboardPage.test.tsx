import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { DashboardPage } from "./DashboardPage";

describe("DashboardPage", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders overview and runtime facts by default", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getByRole("heading", { name: "Dashboard" })).toBeInTheDocument();
    expect(screen.getByText("InMemory")).toBeInTheDocument();
    expect(screen.getByText("Static")).toBeInTheDocument();
    expect(screen.getAllByText("Disabled").length).toBeGreaterThan(0);
  });

  it("shows feature entry cards", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getByRole("button", { name: "Open Tasks" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Open Documents" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Open RAG" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Open Approval" })).toBeInTheDocument();
  });

  it("sends navigation target when shortcut buttons are clicked", () => {
    const onNavigate = vi.fn();
    render(<DashboardPage onNavigate={onNavigate} />);

    fireEvent.click(screen.getByRole("button", { name: "Open Tasks" }));
    fireEvent.click(screen.getByRole("button", { name: "Open Documents" }));
    fireEvent.click(screen.getByRole("button", { name: "Open RAG" }));
    fireEvent.click(screen.getByRole("button", { name: "Open Approval" }));

    expect(onNavigate).toHaveBeenNthCalledWith(1, "analysis");
    expect(onNavigate).toHaveBeenNthCalledWith(2, "documents");
    expect(onNavigate).toHaveBeenNthCalledWith(3, "rag");
    expect(onNavigate).toHaveBeenNthCalledWith(4, "approval");
  });

  it("renders capability boundary without crashing in compact layout", () => {
    render(<DashboardPage onNavigate={vi.fn()} />);

    expect(screen.getAllByText("Keyword Retrieval").length).toBeGreaterThan(0);
    expect(screen.getByText("Not Connected")).toBeInTheDocument();
    expect(screen.getByText("Not Available")).toBeInTheDocument();
  });
});
