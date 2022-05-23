import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PingPage from '../components/PingPage.vue'
import BooksPage from '../components/BooksPage.vue'
import DOMExperiment01 from '../components/DOMExperiment01.vue'
import BookmarksIndex from '../components/BookmarksIndex.vue'
import BookmarksCreate from '../components/BookmarksCreate.vue'
import BookmarksUpdate from '../components/BookmarksUpdate.vue'
import BookmarksImport from '../components/BookmarksImport.vue'
import TagsIndex from '../components/TagsIndex.vue'
import TagsCreate from '../components/TagsCreate.vue'
import TagsUpdate from '../components/TagsUpdate.vue'
import AuthRegister from '../components/AuthRegister.vue'
import AuthLogin from '../components/AuthLogin.vue'

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
    path: '/bookmarks',
    name: 'bookmarks-index',
    component: BookmarksIndex
  },
  {
    path: '/bookmarks/create',
    name: 'bookmarks-create',
    component: BookmarksCreate
  },
  {
    path: '/bookmarks/:id',
    name: 'bookmarks-update',
    component: BookmarksUpdate
  },
  {
    path: '/bookmarks-import',
    name: 'bookmarks-import',
    component: BookmarksImport
  },
  {
    path: '/tags',
    name: 'tags-index',
    component: TagsIndex
  },
  {
    path: '/tags/create',
    name: 'tags-create',
    component: TagsCreate
  },
  {
    path: '/tags/:id',
    name: 'tags-update',
    component: TagsUpdate
  },
  {
    path: '/auth/register',
    name: 'auth-register',
    component: AuthRegister
  },
  {
    path: '/auth/login',
    name: 'auth-login',
    component: AuthLogin
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
