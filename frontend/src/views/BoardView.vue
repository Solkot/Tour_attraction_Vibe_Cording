<template>
  <div class="board-view">
    <div class="board-header">
      <div class="title-area">
        <h2>익명 커뮤니티 게시판</h2>
        <p class="notice">📢 [필독] 마이구미 이용 규칙 (수정/삭제 시 비밀번호가 필요합니다)</p>
      </div>
      <div class="action-area">
        <input type="text" placeholder="🔍 검색어를 입력하세요" class="search-input" />
        <button class="write-btn" @click="$router.push('/board/write')">✍️ 새 글 쓰기</button>
      </div>
    </div>

    <div class="category-filters">
      <button class="filter-btn" :class="{ active: activeCategory === '' }" @click="filterByCategory('')">전체</button>

      <button class="filter-btn" :class="{ active: activeCategory === '관광지' }" @click="filterByCategory('관광지')">🟢
        관광지</button>

      <button class="filter-btn" :class="{ active: activeCategory === '음식점' }" @click="filterByCategory('음식점')">🟡
        음식점</button>

      <button class="filter-btn" :class="{ active: activeCategory === '숙소' }" @click="filterByCategory('숙소')">🔵
        숙소</button>

      <button class="filter-btn" :class="{ active: activeCategory === '쇼핑' }" @click="filterByCategory('쇼핑')">🟣
        쇼핑</button>
    </div>

    <div class="post-list">
      <div class="post-card" v-for="post in posts" :key="post.id" @click="$router.push(`/board/${post.id}`)">
        <div class="post-info">
          <span class="post-no">No. {{ post.id }}</span>
          <span class="post-category">{{ getCategoryIcon(post.category) }}</span>
          <h3 class="post-title">{{ post.title }}</h3>
        </div>
        <div class="post-meta">
          <span>👤 {{ post.author }}</span>
          <span class="divider">|</span>
          <span>👀 조회 {{ post.views }}</span>
        </div>
        <div class="post-date">{{ formatDate(post.created_at) }}</div>
      </div>

      <div v-if="posts.length === 0" style="text-align:center; padding: 40px; color:#64748B;">
        등록된 게시글이 없습니다. 첫 글을 작성해 보세요!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])
const activeCategory = ref('') // 현재 선택된 카테고리 (빈 문자열이면 전체)

const BASE_URL = 'http://192.168.42.82:8000'

// 백엔드에서 게시글 목록 가져오기
const fetchPosts = async (category = '') => {
  try {
    // 카테고리가 선택되어 있으면 파라미터로 같이 보냅니다 (Swagger 명세 반영)
    const params = category ? { category } : {}
    const response = await axios.get(`${BASE_URL}/api/posts`, { params })

    // 받아온 데이터를 posts 배열에 덮어쓰기 (최신 글이 위로 오게 역순 정렬)
    posts.value = response.data.reverse()
  } catch (error) {
    console.error("목록을 불러오는 중 에러 발생:", error)
  }
}

// 화면이 처음 켜질 때 전체 목록 불러오기
onMounted(() => {
  fetchPosts()
})

// 카테고리 버튼 클릭 시 실행할 함수
const filterByCategory = (category) => {
  activeCategory.value = category
  fetchPosts(category)
}

// 백엔드 날짜(2026-07-15T...)를 예쁘게 변환하는 함수
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString() // 예: 2026. 7. 15.
}

// 카테고리 아이콘 변환 함수
const getCategoryIcon = (category) => {
  if (category === '관광지') return '🟢 관광지'
  if (category === '음식점') return '🟡 음식점'
  if (category === '숙소') return '🔵 숙소'
  if (category === '쇼핑') return '🟣 쇼핑'
  return category
}
</script>

<style scoped>
.board-view {
  max-width: 1000px;
  margin: 0 auto;
  background-color: transparent;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20px;
}

.title-area h2 {
  color: #1E293B;
  margin-bottom: 5px;
}

.notice {
  color: #BE123C;
  background-color: #FFE4E6;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  display: inline-block;
  margin: 0;
}

.action-area {
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  width: 250px;
}

.write-btn {
  padding: 10px 20px;
  background-color: #78C2F3;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.category-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: white;
  color: #1E293B;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-btn.active {
  background-color: #78C2F3;
  color: white;
  font-weight: bold;
}

.post-card {
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  position: relative;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-2px);
  transition: 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.post-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.post-no {
  color: #94A3B8;
  font-size: 14px;
}

.post-category {
  color: #0369A1;
  background-color: #E0F2FE;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: bold;
}

.post-title {
  margin: 0;
  font-size: 16px;
  color: #1E293B;
}

.post-meta {
  font-size: 13px;
  color: #64748B;
  display: flex;
  gap: 10px;
  margin-left: 70px;
}

.divider {
  color: #CBD5E1;
}

.post-date {
  position: absolute;
  top: 20px;
  right: 20px;
  color: #94A3B8;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  color: #64748B;
  cursor: pointer;
}

.page-num.active {
  font-weight: bold;
  color: #0369A1;
}
</style>