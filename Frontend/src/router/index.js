import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/shows',
      name: 'shows',
      component: () => import('../views/ShowsView.vue')
    },
    {
      path: '/venues',
      name: 'venues',
      component: () => import('../views/VenuesView.vue')
    },
    {
      path: '/screenings',
      name: 'screenings',
      component: () => import("../views/ScreeningsView.vue")
    },
    {
      path: '/screenings/book',
      name: 'screenings_book',
      component: () => import("../views/ScreeningsBookingView.vue")
    },
    {
      path: '/search',
      name: 'search',
      component: () => import("../views/SearchView.vue")
    },
    {
      path: '/verify_ticket',
      name: 'verify_ticket',
      component: () => import("../views/VerifyTicketView.vue")
    }
  ]
})

export default router
