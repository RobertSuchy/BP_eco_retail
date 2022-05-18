import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/HomePage.vue') }
    ]
  },

  {
    path: '/auth',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'register', name: 'register', meta: { guestOnly: true }, component: () => import('pages/RegisterPage.vue') },
      { path: 'login', name: 'login', meta: { guestOnly: true }, component: () => import('pages/LoginPage.vue') }
    ]
  },

  {
    path: '/user',
    name: 'user',
    meta: { requiresAuth: true },
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'my-account', name: 'myAccount', component: () => import('src/pages/MyAccountPage.vue') },
      { path: 'all-products', name: 'allProducts', component: () => import('src/pages/ProductsPage.vue') },
      { path: 'chain-store', name: 'chainStore', meta: { byUserType: true }, component: () => import('pages/ChainStorePage.vue') },
      { path: 'producer', name: 'producer', meta: { byUserType: true }, component: () => import('pages/ProducerPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
];

export default routes;
