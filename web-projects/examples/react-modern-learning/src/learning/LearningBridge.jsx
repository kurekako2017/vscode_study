import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { getLearningPage, getRouterChildPage } from './registry'
import { recordTrace } from './store'

export function LearningBootTracker() {
  useEffect(() => {
    recordTrace('BOOT', 'main.jsx → App')
  }, [])

  return null
}

export function LearningRouteBridge() {
  const location = useLocation()

  useEffect(() => {
    const page = getLearningPage(location.pathname)
    const childPage = getRouterChildPage(location.pathname)
    recordTrace('ROUTE', `Router → ${page.pageName}`, {
      route: location.pathname,
      routeLabel: location.pathname,
      page,
      childPage,
    })
  }, [location.pathname])

  return null
}
