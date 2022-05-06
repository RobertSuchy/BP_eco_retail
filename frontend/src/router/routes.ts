import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    meta: { requiresAuth: true },
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', name: 'home', component: () => import('pages/HomePage.vue') }]
  },

  {
    path: '/auth',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'register', name: 'register', meta: { guestOnly: true }, component: () => import('pages/RegisterPage.vue') },
      { path: 'login', name: 'login', meta: { guestOnly: true }, component: () => import('pages/LoginPage.vue') }
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
