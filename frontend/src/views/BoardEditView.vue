<template>
  <div class="edit-view" v-if="editPost">
    <div class="header">
      <h2>✏️ 게시글 수정하기</h2>
      <p>수정할 내용을 입력해 주세요.</p>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label>카테고리</label>
        <select class="form-input" v-model="editPost.category">
          <option value="관광지">🟢 관광지</option>
          <option value="음식점">🟡 음식점</option>
          <option value="숙소">🔵 숙소</option>
          <option value="쇼핑">🟣 쇼핑</option>
        </select>
      </div>

      <div class="form-group">
        <label>제목</label>
        <input type="text" class="form-input" v-model="editPost.title" />
      </div>

      <div class="form-group">
        <label>내용</label>
        <textarea class="form-input textarea" rows="10" v-model="editPost.content"></textarea>
      </div>

      <div class="button-group">
        <button class="btn-cancel" @click="$router.push(`/board/${route.params.id}`)">취소</button>
        <button class="btn-submit" @click="submitEdit">수정 완료</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useBoardStore } from '../stores/boardStore';

const route = useRoute();
const router = useRouter();
const boardStore = useBoardStore();

const editPost = ref(null);

// 화면 켜질 때 기존 데이터 불러와서 입력창에 채워넣기
onMounted(() => {
  const postId = route.params.id;
  const originalPost = boardStore.getPostById(postId);
  
  if (originalPost) {
    // 깊은 복사(Object.assign)를 해서 수정 중 취소해도 원본이 망가지지 않게 함
    editPost.value = { ...originalPost };
  } else {
    alert('잘못된 접근입니다.');
    router.push('/board');
  }
});

// 수정 완료 버튼 눌렀을 때
const submitEdit = () => {
  if (!editPost.value.title || !editPost.value.content) {
    alert('제목과 내용을 모두 입력해 주세요!');
    return;
  }

  // Pinia 저장소 업데이트 함수 호출
  boardStore.updatePost(route.params.id, {
    category: editPost.value.category,
    title: editPost.value.title,
    content: editPost.value.content
  });
  
  alert('수정이 완료되었습니다!');
  router.push(`/board/${route.params.id}`); // 다시 상세보기 화면으로 이동
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