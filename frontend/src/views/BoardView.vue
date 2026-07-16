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
      <button class="filter-btn" :class="{ active: activeCategory === '관광지' }" @click="filterByCategory('관광지')">🏛️ 관광지</button>
      <button class="filter-btn" :class="{ active: activeCategory === '숙박' }" @click="filterByCategory('숙박')">⛺ 숙박</button>
      <button class="filter-btn" :class="{ active: activeCategory === '쇼핑' }" @click="filterByCategory('쇼핑')">🛒 쇼핑</button>
      <button class="filter-btn" :class="{ active: activeCategory === '음식점' }" @click="filterByCategory('음식점')">🍽️ 음식점</button>
      <button class="filter-btn" :class="{ active: activeCategory === '문화시설' }" @click="filterByCategory('문화시설')">🎨 문화시설</button>
      <button class="filter-btn" :class="{ active: activeCategory === '축제공연행사' }" @click="filterByCategory('축제공연행사')">🎉 축제공연행사</button>
      <button class="filter-btn" :class="{ active: activeCategory === '여행코스' }" @click="filterByCategory('여행코스')">🗺️ 여행코스</button>
      <button class="filter-btn" :class="{ active: activeCategory === '레포츠' }" @click="filterByCategory('레포츠')">🏄 레포츠</button>
    </div>

    <div class="post-list">
      <div class="post-card" v-for="post in posts" :key="post.id" @click="$router.push(`/board/${post.id}`)">
        <div class="post-info">
          <span class="post-no">No. {{ post.id }}</span>
          <span class="post-category">{{ getCategoryIcon(post.category) }}</span>
          <h3 class="post-title">{{ post.title }}</h3>
        </div>
        <div class="post-meta">
          <span>{{ getAuthorEmoji(post.id) }} {{ post.author }}</span>
          <span class="divider">|</span>
          <span>조회수 {{ post.views }}</span>
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

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

// 백엔드에서 게시글 목록 가져오기
const fetchPosts = async (category = '') => {
  try {
    const params = category ? { category } : {}
    const response = await axios.get(`${BASE_URL}/api/posts`, { params })

    // 🌟 reverse() 대신 확실하게 id 기준으로 내림차순(최신순) 정렬!
    posts.value = response.data.sort((a, b) => b.id - a.id)
  } catch (error) {
    console.error("목록을 불러오는 중 에러 발생:", error)
  }
}

const emoticons = ['🐰', '🦊', '🐻', '🐼', '🐯', '🦁', '🐨', '🐸', '🐹', '🐭', '🐱', '🐶', '🦄', '🦦', '🦥']


const getAuthorEmoji = (id) => {
  if (!id) return '👤' // id가 없을 경우 기본값
  return emoticons[id % emoticons.length] 
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

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString() 
}

const getCategoryIcon = (category) => {
  if (category === '관광지') return '🏛️ 관광지'
  if (category === '숙박') return '⛺ 숙박'
  if (category === '쇼핑') return '🛒 쇼핑'
  if (category === '음식점') return '🍽️ 음식점'
  if (category === '문화시설') return '🎨 문화시설'
  if (category === '축제공연행사') return '🎉 축제공연행사'
  if (category === '여행코스') return '🗺️ 여행코스'
  if (category === '레포츠') return '🏄 레포츠'
  return category
}

</script>

<style scoped>
.board-view {
  max-width: 2200px;
  margin: 0 auto;
  padding: 20px;
  background-color: transparent;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.title-area h2 {
  color: #0369A1;
  /* 더 쨍하고 예쁜 파란색 */
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 8px;
}

.notice {
  color: #E11D48;
  /* 세련된 장미색 */
  background-color: #FFF1F2;
  padding: 8px 16px;
  border-radius: 12px;
  /* 더 동글동글하게 */
  font-size: 14px;
  font-weight: 800;
  display: inline-block;
  margin: 0;
  box-shadow: 0 4px 6px rgba(225, 29, 72, 0.05);
}

.action-area {
  display: flex;
  gap: 12px;
}

.search-input {
  padding: 12px 20px;
  border: 2px solid #E2E8F0;
  border-radius: 12px;
  width: 280px;
  font-size: 15px;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #38BDF8;
  box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15);
  /* 파란색 포커스 링 */
}

.write-btn {
  padding: 12px 24px;
  background-color: #78C2F3;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(120, 194, 243, 0.3);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.write-btn:hover {
  background-color: #38BDF8;
  transform: translateY(-3px);
  /* 둥둥 떠오름 */
  box-shadow: 0 6px 15px rgba(56, 189, 248, 0.4);
}

/* 🌟 4. 카테고리 필터 버튼 */
.category-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  /* 모바일 대응 */
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid transparent;
  border-radius: 25px;
  background-color: #F1F5F9;
  color: #64748B;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background-color: #E0F2FE;
  color: #0369A1;
  transform: translateY(-2px);
}

.filter-btn.active {
  background-color: #38BDF8;
  color: white;
  box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
}

/* 🌟 5. 게시글 카드 (디자인의 꽃!) */
.post-card {
  background-color: white;
  padding: 25px;
  border-radius: 20px;
  border: 1px solid #F0F8FF;
  margin-bottom: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  position: relative;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.post-card:hover {
  transform: translateY(-5px);
  /* 위로 뿅! */
  border-color: #BAE6FD;
  box-shadow: 0 12px 25px rgba(120, 194, 243, 0.15);
  /* 하늘색 그림자 */
}

.post-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 12px;
}

.post-no {
  color: #94A3B8;
  font-size: 14px;
  font-weight: bold;
  width: 45px;
}

.post-category {
  color: #0369A1;
  background-color: #E0F2FE;
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 800;
}

.post-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #1E293B;
  /* 글이 너무 길면 ... 처리 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 70%;
}

.post-meta {
  font-size: 14px;
  color: #64748B;
  display: flex;
  gap: 12px;
  margin-left: 60px;
  /* 번호와 카테고리 너비만큼 띄움 */
}

.divider {
  color: #CBD5E1;
}

.post-date {
  position: absolute;
  top: 25px;
  right: 25px;
  color: #94A3B8;
  font-size: 14px;
}

/* 🌟 6. 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 40px;
  margin-bottom: 20px;
  color: #64748B;
  cursor: pointer;
}

.page-num {
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.page-num:hover {
  background-color: #F1F5F9;
  color: #1E293B;
}

.page-num.active {
  background-color: #78C2F3;
  color: white;
  font-weight: 800;
  box-shadow: 0 4px 10px rgba(120, 194, 243, 0.3);
}

/* 📱 7. 모바일 반응형 */
@media screen and (max-width: 768px) {
  .board-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-area {
    width: 100%;
    flex-direction: column;
    /* 검색창과 버튼을 세로로 */
  }

  .search-input {
    width: 100%;
    /* 모바일 화면에 꽉 차게 */
    box-sizing: border-box;
  }

  .write-btn {
    width: 100%;
  }

  .post-title {
    max-width: 100%;
    /* 모바일에서는 제목을 전체 너비로 */
  }

  /* 모바일에서는 날짜가 우측 상단 고정이 아니라 아래로 내려오게 */
  .post-date {
    position: static;
    margin-left: 60px;
    margin-top: 5px;
    font-size: 13px;
  }

  .post-meta {
    margin-bottom: 5px;
  }
}
</style>