import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PingPage from '../components/PingPage.vue'
import BooksPage from '../components/BooksPage.vue'
import DOMExperiment01 from '../components/DOMExperiment01.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/dom-experiment-01',
    name: 'dom-experiment-01',
    component: DOMExperiment01
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/books-page',
    name: 'books-page',
    component: BooksPage
  },
  {
    path: '/ping-page',
    name: 'ping-page',
    component: PingPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
