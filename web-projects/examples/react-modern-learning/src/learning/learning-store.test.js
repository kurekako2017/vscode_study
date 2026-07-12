import { describe, expect, it, beforeEach } from 'vitest'
import { getLearningState, learningPages, recordTrace, resetLearningStore } from './index'

describe('learning store', () => {
  beforeEach(() => {
    resetLearningStore()
  })

  it('records trace entries and state changes', () => {
    recordTrace('BOOT', 'main.jsx → App')
    recordTrace('STATE', 'count:0→1', { reason: 'CounterDemo count' })

    const snapshot = getLearningState()

    expect(snapshot.traces).toHaveLength(2)
    expect(snapshot.lastStateChange).toBe('count:0→1')
    expect(snapshot.lastRenderReason).toBe('CounterDemo count')
  })

  it('keeps the real page registry for learning panel data', () => {
    expect(learningPages.find((page) => page.route === '/hooks')?.sourceFiles).toContain(
      'src/chapters/hooks/useEffect/TimerDemo.jsx',
    )
  })
})
