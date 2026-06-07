import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import Counter from './Counter'

describe('Counter', () => {
  it('increments count when clicked', () => {
    render(<Counter />)

    fireEvent.click(screen.getByRole('button', { name: '+1' }))

    expect(screen.getByText(/当前值：1/)).toBeInTheDocument()
  })
})
