<template>
  <div class="edit-view">
    <div class="header">
      <h2>✏️ 게시글 수정하기</h2>
      <p>수정할 내용을 입력해 주세요.</p>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label>카테고리</label>
        <select class="form-input" v-model="category">
          <option value="관광지">🟢 관광지</option>
          <option value="음식점">🟡 음식점</option>
          <option value="숙소">🔵 숙소</option>
          <option value="쇼핑">🟣 쇼핑</option>
        </select>
      </div>

      <div class="form-group">
        <label>제목</label>
        <input type="text" class="form-input" v-model="title" />
      </div>

      <div class="form-group">
        <label>내용</label>
        <textarea class="form-input textarea" rows="10" v-model="content"></textarea>
      </div>

      <div class="button-group">
        <!-- 취소 시 상세 화면으로 돌아감 -->
        <button class="btn-cancel" @click="$router.push('/board/1')">취소</button>
        <button class="btn-submit" @click="submitEdit">수정 완료</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 임시 더미 데이터 (나중에는 백엔드에서 받아온 데이터를 넣습니다)
const category = ref('관광지');
const title = ref('금오산 둘레길 지금 단풍 상태 완전 절정이에요! 🍁');
const content = ref('이번 주말에 금오산 다녀왔는데 단풍이 정말 예쁘게 물들었네요.\n가족들과 산책 다녀오기 딱 좋은 날씨입니다. 강추해요!');

const submitEdit = () => {
  // TODO: 백엔드 수정 API 연결
  alert('수정이 완료되었습니다!');
};
</script>

<style scoped>
.edit-view { max-width: 800px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
.header { margin-bottom: 30px; border-bottom: 2px solid #F0F8FF; padding-bottom: 20px; }
.header h2 { color: #1E293B; margin: 0 0 10px 0; }
.header p { color: #64748B; margin: 0; }
.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
.form-group label { font-weight: bold; color: #1E293B; margin-bottom: 8px; font-size: 14px; }
.form-input { padding: 12px; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 15px; }
.form-input:focus { outline: none; border-color: #78C2F3; }
.textarea { resize: vertical; }
.button-group { display: flex; justify-content: flex-end; gap: 10px; margin-top: 30px; }
button { padding: 12px 24px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; }
.btn-cancel { background-color: #F1F5F9; color: #64748B; }
.btn-submit { background-color: #78C2F3; color: white; }
</style>