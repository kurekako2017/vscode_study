import { useCallback, useEffect, useState } from 'react'
import { formatLearningValue, recordTrace } from './store'

export function useLearningLifecycle(name) {
  useEffect(() => {
    recordTrace('COMPONENT', `${name} mount`)
  }, [name])

  useEffect(() => {
    recordTrace('RENDER', `${name} render`)
  })
}

export function useLearningHookSnapshot(componentName, hookName, value, label) {
  useEffect(() => {
    const summary = label ?? formatLearningValue(value)
    recordTrace('HOOK', `${componentName} ${hookName}${summary ? ` ${summary}` : ''}`, {
      snapshot: {
        componentName,
        hookName,
        label: label ?? '',
        summary,
        value,
      },
    })
  }, [componentName, hookName, value, label])
}

export function useLearningState(componentName, stateName, initialValue) {
  const [value, setValue] = useState(initialValue)

  useLearningHookSnapshot(componentName, 'useState()', value, `${stateName}=${formatLearningValue(value)}`)

  const setTrackedValue = useCallback(
    (nextValue) => {
      setValue((currentValue) => {
        const resolvedValue = typeof nextValue === 'function' ? nextValue(currentValue) : nextValue
        recordTrace('STATE', `${stateName}:${formatLearningValue(currentValue)}→${formatLearningValue(resolvedValue)}`, {
          reason: `${componentName} ${stateName}`,
        })
        return resolvedValue
      })
    },
    [componentName, stateName],
  )

  return [value, setTrackedValue]
}

export function useLearningEffect(componentName, effectName, effect, dependencies) {
  useEffect(() => {
    recordTrace('EFFECT', `${componentName} ${effectName}`)
    const cleanup = effect?.()

    return () => {
      recordTrace('CLEANUP', `${componentName} ${effectName}`)
      if (typeof cleanup === 'function') {
        cleanup()
      }
    }
  }, dependencies)
}

export function traceEvent(message, data) {
  recordTrace('EVENT', message, data)
}

export function traceCall(message, data) {
  recordTrace('CALL', message, data)
}

export function traceError(message, data) {
  recordTrace('ERROR', message, data)
}
