// 让 Vitest 在测试环境里拥有 jest-dom 的额外断言能力。
// 例如 toBeInTheDocument() 就来自这里。
// 这类全局初始化文件通常只做一次性配置，避免每个测试都重复写。
import '@testing-library/jest-dom/vitest'
