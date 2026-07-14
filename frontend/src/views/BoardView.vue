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
      <button class="filter-btn active">전체</button>
      <button class="filter-btn">🟢 관광지</button>
      <button class="filter-btn">🟡 음식점</button>
      <button class="filter-btn">🔵 숙소</button>
      <button class="filter-btn">🟣 쇼핑</button>
    </div>

    <div class="post-list">
      <div class="post-card" v-for="i in 4" :key="i" @click="$router.push('/board/1')">
        <div class="post-info">
          <span class="post-no">No. {{ 5 - i }}</span>
          <span class="post-category">🟢 관광지</span>
          <h3 class="post-title">금오산 둘레길 지금 단풍 상태 완전 절정이에요! 🍁</h3>
        </div>
        <div class="post-meta">
          <span>👤 익명작성자</span>
          <span class="divider">|</span>
          <span>💬 댓글 3</span>
          <span class="divider">|</span>
          <span>👀 조회 142</span>
        </div>
        <div class="post-date">2026.07.14</div>
      </div>
    </div>

    <div class="pagination">
      <span>◀</span>
      <span class="page-num active">1</span>
      <span class="page-num">2</span>
      <span class="page-num">3</span>
      <span>▶</span>
    </div>
  </div>
</template>

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
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
  position: relative;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-2px);
  transition: 0.2s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
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