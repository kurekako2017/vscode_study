import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import Counter from './Counter'

describe('Counter', () => {
  it('increments count when clicked', () => {
    // render 会把组件渲染到测试环境里，后面才能像用户一样操作它。
    render(<Counter />)

    // fireEvent.click 模拟真实用户点击按钮。
    fireEvent.click(screen.getByRole('button', { name: '+1' }))

    // 断言时不要只依赖正则文本，因为文本可能被拆到不同标签里。
    // 这里直接检查元素的完整 textContent，会更稳定。
    expect(screen.getByText((_, element) => element?.textContent === '当前值：1')).toBeInTheDocument()
  })
})
