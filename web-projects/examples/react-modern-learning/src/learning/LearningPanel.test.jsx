import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import LearningPanel from './LearningPanel'
import { learningPages, recordTrace, resetLearningStore } from './index'

describe('LearningPanel', () => {
  beforeEach(() => {
    resetLearningStore()
  })

  it('shows route, component tree, source files, and traces', () => {
    const hooksPage = learningPages.find((page) => page.route === '/hooks')

    recordTrace('ROUTE', 'Router → HooksPage', {
      route: '/hooks',
      routeLabel: '/hooks',
      page: hooksPage,
      childPage: 'HooksPage',
    })
    recordTrace('HOOK', 'CounterDemo useState() count=0', {
      snapshot: {
        componentName: 'CounterDemo',
        hookName: 'useState()',
        label: 'count=0',
        summary: 'count=0',
        value: 0,
      },
    })
    recordTrace('STATE', 'count:0→1', { reason: 'CounterDemo count' })

    render(<LearningPanel />)

    expect(screen.getByText('Current Route')).toBeInTheDocument()
    expect(screen.getByText('/hooks')).toBeInTheDocument()
    expect(screen.getByText('HooksPage')).toBeInTheDocument()
    expect(screen.getAllByText((_, element) => element?.textContent?.includes('CounterDemo'))[0]).toBeInTheDocument()
    expect(screen.getByText('src/chapters/hooks/useEffect/TimerDemo.jsx')).toBeInTheDocument()
    expect(screen.getByText('Recent Trace')).toBeInTheDocument()
    expect(screen.getAllByText((_, element) => element?.textContent?.includes('count:0→1'))[0]).toBeInTheDocument()
  })
})
