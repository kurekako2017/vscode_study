import { useSyncExternalStore } from 'react'

const MAX_TRACE_ENTRIES = 60

const initialState = {
  bootLabel: '',
  currentRoute: '/',
  currentRouteLabel: '/',
  currentPageId: 'home',
  currentPageName: 'HomePage',
  currentChildPage: 'HomePage',
  componentTree: [],
  hooksUsed: [],
  propsFlow: [],
  sourceFiles: [],
  testFile: null,
  hookSnapshots: [],
  lastComponent: '',
  lastEvent: '',
  lastStateChange: '',
  lastRenderReason: '',
  lastEffect: '',
  lastCleanup: '',
  lastError: '',
  traces: [],
}

let state = initialState
const listeners = new Set()
let nextTraceId = 1

function notify() {
  for (const listener of listeners) {
    listener()
  }
}

function toText(value) {
  if (typeof value === 'string') {
    return value
  }

  if (typeof value === 'number' || typeof value === 'boolean' || value == null) {
    return String(value)
  }

  if (Array.isArray(value)) {
    return `[${value.map((item) => toText(item)).join(', ')}]`
  }

  try {
    return JSON.stringify(value)
  } catch {
    return Object.prototype.toString.call(value)
  }
}

function upsertHookSnapshot(snapshots, snapshot) {
  const key = `${snapshot.componentName}:${snapshot.hookName}:${snapshot.label ?? ''}`
  const nextSnapshots = snapshots.filter((item) => item.key !== key)

  nextSnapshots.push({
    ...snapshot,
    key,
  })

  return nextSnapshots
}

function applyTraceEffects(previousState, entry) {
  const nextState = { ...previousState, traces: [...previousState.traces, entry].slice(-MAX_TRACE_ENTRIES) }

  switch (entry.type) {
    case 'BOOT':
      nextState.bootLabel = entry.message
      return nextState
    case 'ROUTE':
      nextState.currentRoute = entry.data.route ?? previousState.currentRoute
      nextState.currentRouteLabel = entry.data.routeLabel ?? entry.data.route ?? previousState.currentRouteLabel
      nextState.currentPageId = entry.data.page?.id ?? previousState.currentPageId
      nextState.currentPageName = entry.data.page?.pageName ?? previousState.currentPageName
      nextState.currentChildPage = entry.data.childPage ?? entry.data.page?.childPage ?? previousState.currentChildPage
      nextState.componentTree = entry.data.page?.componentTree ?? previousState.componentTree
      nextState.hooksUsed = entry.data.page?.hooksUsed ?? previousState.hooksUsed
      nextState.propsFlow = entry.data.page?.propsFlow ?? previousState.propsFlow
      nextState.sourceFiles = entry.data.page?.sourceFiles ?? previousState.sourceFiles
      nextState.testFile = entry.data.page?.testFile ?? previousState.testFile
      nextState.hookSnapshots = []
      nextState.lastRenderReason = `路由切换到 ${nextState.currentPageName}`
      return nextState
    case 'COMPONENT':
      nextState.lastComponent = entry.message
      return nextState
    case 'HOOK':
      nextState.hookSnapshots = upsertHookSnapshot(previousState.hookSnapshots, entry.data.snapshot)
      return nextState
    case 'EVENT':
      nextState.lastEvent = entry.message
      nextState.lastRenderReason = entry.data.reason ?? entry.message
      return nextState
    case 'CALL':
      nextState.lastEvent = entry.message
      nextState.lastRenderReason = entry.data.reason ?? entry.message
      return nextState
    case 'STATE':
      nextState.lastStateChange = entry.message
      nextState.lastRenderReason = entry.data.reason ?? entry.message
      return nextState
    case 'RENDER':
      nextState.lastRenderReason = entry.data.reason ?? entry.message
      return nextState
    case 'EFFECT':
      nextState.lastEffect = entry.message
      return nextState
    case 'CLEANUP':
      nextState.lastCleanup = entry.message
      return nextState
    case 'ERROR':
      nextState.lastError = entry.message
      return nextState
    default:
      return nextState
  }
}

export function recordTrace(type, message, data = {}) {
  const entry = {
    id: nextTraceId,
    type,
    message,
    data,
    timestamp: Date.now(),
  }

  nextTraceId += 1
  console.info(`[${String(entry.id).padStart(3, '0')}] ${message}`)
  state = applyTraceEffects(state, entry)
  notify()
  return entry
}

export function resetLearningStore() {
  state = { ...initialState, traces: [] }
  nextTraceId = 1
  notify()
}

export function setLearningRoute(routeInfo) {
  state = applyTraceEffects(state, {
    id: nextTraceId++,
    type: 'ROUTE',
    message: routeInfo.page?.pageName ? `Router → ${routeInfo.page.pageName}` : `Router → ${toText(routeInfo.route)}`,
    data: routeInfo,
    timestamp: Date.now(),
  })
  notify()
}

export function setLearningBoot(label) {
  state = applyTraceEffects(state, {
    id: nextTraceId++,
    type: 'BOOT',
    message: label,
    data: {},
    timestamp: Date.now(),
  })
  notify()
}

export function useLearningStore(selector = (currentState) => currentState) {
  return useSyncExternalStore(
    (listener) => {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
    () => selector(state),
    () => selector(state),
  )
}

export function getLearningState() {
  return state
}

export function formatLearningValue(value) {
  return toText(value)
}
