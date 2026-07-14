import { createRouter, createWebHistory } from 'vue-router'
import MapView from '../views/MapView.vue'
import BoardView from '../views/BoardView.vue'
import MyCourseView from '../views/MyCourseView.vue'

const routes = [
  { path: '/', component: MapView },            // 기본 메인 화면 (지도)
  { path: '/board', component: BoardView },     // 익명 게시판 화면
  { path: '/course', component: MyCourseView }  // 마이 코스 화면
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router