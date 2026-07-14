<template>
  <div class="write-view">
    <div class="header">
      <h2>✍️ 새 글 쓰기</h2>
      <p>구미 여행 꿀팁을 익명으로 자유롭게 남겨주세요.</p>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label>카테고리</label>
        <select class="form-input">
          <option value="관광지">🟢 관광지</option>
          <option value="음식점">🟡 음식점</option>
          <option value="숙소">🔵 숙소</option>
          <option value="쇼핑">🟣 쇼핑</option>
        </select>
      </div>

      <div class="form-group">
        <label>제목</label>
        <input type="text" class="form-input" placeholder="게시글 제목을 입력하세요" />
      </div>

      <!-- 요구사항 '나': 수정용 비밀번호 입력 -->
      <div class="form-group">
        <label>수정용 비밀번호 (필수)</label>
        <input type="password" class="form-input" placeholder="수정/삭제 시 사용할 비밀번호 (숫자 4자리 권장)" />
        <small class="help-text">※ 비밀번호를 분실하면 글을 수정하거나 삭제할 수 없습니다.</small>
      </div>

      <div class="form-group">
        <label>내용</label>
        <textarea class="form-input textarea" rows="10" placeholder="내용을 입력하세요"></textarea>
      </div>

      <div class="button-group">
        <button class="btn-cancel" @click="$router.push('/board')">취소</button>
        <button class="btn-submit">등록하기</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.write-view {
  max-width: 800px;
  margin: 0 auto;
  background-color: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.header { margin-bottom: 30px; border-bottom: 2px solid #F0F8FF; padding-bottom: 20px; }
.header h2 { color: #1E293B; margin: 0 0 10px 0; }
.header p { color: #64748B; margin: 0; }

.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
.form-group label { font-weight: bold; color: #1E293B; margin-bottom: 8px; font-size: 14px; }
.form-input { padding: 12px; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 15px; }
.form-input:focus { outline: none; border-color: #78C2F3; }
.textarea { resize: vertical; }

.help-text { color: #BE123C; font-size: 12px; margin-top: 5px; }

.button-group { display: flex; justify-content: flex-end; gap: 10px; margin-top: 30px; }
button { padding: 12px 24px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; }
.btn-cancel { background-color: #F1F5F9; color: #64748B; }
.btn-submit { background-color: #78C2F3; color: white; }
</style>