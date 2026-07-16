import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MapView from '../views/MapView.vue'
import BoardView from '../views/BoardView.vue'
import BoardWriteView from '../views/BoardWriteView.vue'
import BoardDetailView from '../views/BoardDetailView.vue'
import BoardEditView from '../views/BoardEditView.vue'
import MyCourseView from '../views/MyCourseView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/map', component: MapView },
  { path: '/board', component: BoardView },
  { path: '/board/write', component: BoardWriteView },
  { path: '/board/:id', component: BoardDetailView },
  { path: '/board/edit/:id', component: BoardEditView },
  { path: '/course', component: MyCourseView }       
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })

export default router