import { useEffect, useState } from "react";

const NAVIGATION_EVENT = "erip:navigation";

interface NavigateOptions {
  replace?: boolean;
  state?: Record<string, unknown>;
}

/** 使用浏览器 History API 保持零新增依赖，同时让刷新和直达 URL 有明确语义。 */
export function navigateTo(path: string, options: NavigateOptions = {}) {
  if (options.replace) {
    window.history.replaceState(options.state ?? null, "", path);
  } else {
    window.history.pushState(options.state ?? null, "", path);
  }
  window.dispatchEvent(new Event(NAVIGATION_EVENT));
}

export function useCurrentPath(): string {
  const [path, setPath] = useState(window.location.pathname);
  useEffect(() => {
    const update = () => setPath(window.location.pathname);
    window.addEventListener("popstate", update);
    window.addEventListener(NAVIGATION_EVENT, update);
    return () => {
      window.removeEventListener("popstate", update);
      window.removeEventListener(NAVIGATION_EVENT, update);
    };
  }, []);
  return path;
}
