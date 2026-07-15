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
          <option value="관광지">🏛️ 관광지</option>
          <option value="음식점">🍽️ 음식점</option>
          <option value="숙소">⛺ 숙소</option>
          <option value="쇼핑">🛒 쇼핑</option>
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

      <div class="form-group">
        <label>비밀번호 확인 (필수)</label>
        <input type="password" class="form-input" v-model="editPost.password" placeholder="게시글 작성 시 설정한 비밀번호를 입력하세요" />
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
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const BASE_URL = 'http://192.168.42.82:8000';

// 수정할 데이터를 담을 변수 (비밀번호 포함)
const editPost = ref({
  category: '관광지',
  title: '',
  content: '',
  password: ''
});

// 화면이 켜질 때 기존 데이터 불러오기 (GET)
onMounted(async () => {
  try {
    const postId = route.params.id;
    const response = await axios.get(`${BASE_URL}/api/posts/${postId}`);
    
    // 가져온 데이터를 입력창에 미리 채워주기
    editPost.value.title = response.data.title;
    editPost.value.content = response.data.content;
    editPost.value.category = response.data.category;
    // 비밀번호는 비워둡니다 (사용자가 직접 쳐야 함)
    
  } catch (error) {
    alert('기존 게시글을 불러오는데 실패했습니다.');
    router.push('/board');
  }
});

// 수정 완료 버튼 클릭 시 실행 (PUT)
const submitEdit = async () => {
  if (!editPost.value.title || !editPost.value.content || !editPost.value.password) {
    alert('제목, 내용, 비밀번호를 모두 입력해 주세요!');
    return;
  }

  try {
    const postId = route.params.id;
    const payload = {
      title: editPost.value.title,
      content: editPost.value.content,
      category: editPost.value.category,
      password: editPost.value.password
    };

    // 백엔드로 PUT 요청 쏘기
    await axios.put(`${BASE_URL}/api/posts/${postId}`, payload);
    
    alert('수정이 완료되었습니다!');
    router.push(`/board/${postId}`); // 다시 상세 화면으로 이동
    
  } catch (error) {
    console.error('수정 에러:', error);
    // 에러 상태 코드에 따른 알림 처리 (비밀번호 틀림 등)
    if (error.response && error.response.status === 400) {
      alert('비밀번호가 일치하지 않습니다.');
    } else {
      alert('수정에 실패했습니다. 비밀번호를 다시 확인해 주세요.');
    }
  }
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