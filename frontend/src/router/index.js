import { createRouter, createWebHistory } from 'vue-router'
import MapView from '../views/MapView.vue'
import BoardView from '../views/BoardView.vue'
import BoardWriteView from '../views/BoardWriteView.vue'   // 글쓰기 화면
import BoardDetailView from '../views/BoardDetailView.vue' // 상세 조회 화면
import BoardEditView from '../views/BoardEditView.vue'
import MyCourseView from '../views/MyCourseView.vue'

const routes = [
  { path: '/', component: MapView },            // 기본 메인 화면 (지도)
  { path: '/board', component: BoardView },     // 익명 게시판 화면
  { path: '/board/write', component: BoardWriteView },     // 글쓰기 주소
  { path: '/board/:id', component: BoardDetailView },      // 상세 조회 주소 (id값에 따라 바뀜)
  { path: '/board/edit/:id', component: BoardEditView },
  { path: '/course', component: MyCourseView }  // 마이 코스 화면
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router