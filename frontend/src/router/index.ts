import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // Lazy-loaded route (better for performance)
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LogInView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUpView.vue')
    },
    {
      path: '/add-workout',
      name: 'add-workout',
      component: () => import('../views/AddWorkoutView.vue')
    },
    {
      path: '/update-workout',
      name: 'update-workout',
      component: () => import('../views/UpdateWorkoutView.vue')
    }

  ]
})

export default router