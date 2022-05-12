import { boot } from 'quasar/wrappers'
import { authManager } from 'src/services'
import { RouteLocationNormalized, RouteLocationRaw } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean,
    guestOnly?: boolean,
    byUserType?: boolean
  }
}

const loginRoute = (from: RouteLocationNormalized): RouteLocationRaw => {
  return {
    name: 'login',
    query: { redirect: from.fullPath }
  }
}

// this boot file wires together authentication handling with router
export default boot(({ router, store }) => {
  // if the token was removed from storage, redirect to login
  authManager.onLogout(() => {
    router.push(loginRoute(router.currentRoute.value))
  })

  // add route guard to check auth user
  router.beforeEach(async (to) => {
    const isAuthenticated = await store.dispatch('auth/check')

    // route requires authentication
    if (to.meta.requiresAuth && !isAuthenticated) {
      // check if logged in if not, redirect to login page
      return loginRoute(to)
    }

    // route is only for guests so redirect to home
    if (to.meta.guestOnly && isAuthenticated) {
      return { name: 'home' }
    }

    if (to.meta.byUserType && isAuthenticated) {
      const userType = store.state.auth.user.userType
      if (to.name !== userType) {
        switch (userType) {
          case 'customer': {
            return { name: 'customer' }
          }
          case 'chainStore': {
            return { name: 'chainStore' }
          }
          case 'producer': {
            return { name: 'producer' }
          }
        }
      }
    }
  })
})
