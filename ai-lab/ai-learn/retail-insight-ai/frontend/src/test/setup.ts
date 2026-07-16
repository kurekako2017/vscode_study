// 扩展 Vitest 断言，使组件测试可以直接判断元素是否存在和包含文本。
import "@testing-library/jest-dom/vitest";
import { afterEach } from "vitest";

import { resetApiAuthForTests } from "../api";

afterEach(() => {
  resetApiAuthForTests();
  sessionStorage.clear();
  window.history.replaceState(null, "", "/");
});
