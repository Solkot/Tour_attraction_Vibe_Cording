<template>
  <div class="detail-view" v-if="post">
    <div class="post-card">
      <div class="post-header">
        <span class="category-badge">{{ post.category }}</span>
        <h2 class="title">{{ post.title }}</h2>
        <div class="meta-info">
          <span>👤 {{ post.author }}</span> | <span>{{ formatDate(post.created_at) }}</span> | <span>👀 조회 {{ post.views
            }}</span>
        </div>
      </div>

      <div class="post-content">
        <p v-html="post.content.replace(/\n/g, '<br>')"></p>
      </div>

      <div class="action-buttons">
        <button class="btn-list" @click="$router.push('/board')">목록</button>
        <div class="right-buttons">
          <button class="btn-edit" @click="openPasswordModal('수정')">수정</button>
          <button class="btn-delete" @click="openPasswordModal('삭제')">삭제</button>
        </div>
      </div>

      <div class="comments-section">
        <h3 class="comments-title">💬 댓글</h3>

        <div class="comment-write-box">
          <input type="password" v-model="newCommentPassword" placeholder="비밀번호" class="comment-pw-input" />
          <input type="text" v-model="newCommentContent" placeholder="따뜻한 댓글을 남겨주세요..." class="comment-text-input"
            @keyup.enter="submitComment" />
          <button class="btn-comment-submit" @click="submitComment">등록</button>
        </div>

        <div class="comment-list">
          <div v-if="comments.length === 0" class="empty-comment">
            아직 작성된 댓글이 없습니다. 첫 번째 댓글을 남겨보세요!
          </div>

          <div v-else class="comment-item" v-for="comment in comments" :key="comment.id">
            <div class="comment-info">
              <span class="comment-author">👤 {{ comment.author }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div class="comment-content">{{ comment.content }}</div>

            <button class="btn-delete-comment" @click="deleteComment(comment.id)">❌</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-overlay" v-if="showModal">
      <div class="password-modal">
        <h3>🔒 비밀번호 확인</h3>
        <p>게시글을 {{ modalAction }}하려면 비밀번호를 입력하세요.</p>
        <input type="password" v-model="inputPassword" placeholder="비밀번호 입력" class="modal-input" />
        <div class="modal-buttons">
          <button class="btn-cancel" @click="showModal = false">취소</button>
          <button class="btn-submit" @click="verifyPassword">확인</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else style="text-align:center; padding:50px;">
    <h2>존재하지 않는 게시글입니다.</h2>
    <button @click="$router.push('/board')">목록으로 돌아가기</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const post = ref(null);
const showModal = ref(false);
const modalAction = ref('');
const inputPassword = ref('');
const newCommentContent = ref('');
const newCommentPassword = ref('');
const comments = ref([]);

const BASE_URL = 'http://192.168.42.82:8000';

// 상세 데이터 불러오기
const fetchPostDetail = async () => {
  try {
    const postId = route.params.id;
    const response = await axios.get(`${BASE_URL}/api/posts/${postId}`);
    post.value = response.data;
  } catch (error) {
    console.error("상세 정보 에러:", error);
    alert("존재하지 않거나 삭제된 게시글입니다.");
    router.push('/board'); // 에러 나면 목록으로 강제 복귀
  }
};

onMounted(() => {
  fetchPostDetail();
  fetchComments();
});

// 백엔드 날짜 변환 함수
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString().slice(0, 5);
};

const openPasswordModal = (action) => {
  if (action === '수정') {
    router.push(`/board/edit/${route.params.id}`);
  } else {
    modalAction.value = action;
    inputPassword.value = '';
    showModal.value = true;
  }
};

// 비밀번호 검증 및 삭제 실행 (DELETE)
const verifyPassword = async () => {
  if (!inputPassword.value) {
    alert("비밀번호를 입력해주세요.");
    return;
  }

  if (modalAction.value === '삭제') {
    try {
      const postId = route.params.id;

      // 💡 핵심: Swagger 명세에 따라 password를 query 파라미터로 보냅니다!
      await axios.delete(`${BASE_URL}/api/posts/${postId}`, {
        params: { password: inputPassword.value }
      });

      alert('게시글이 성공적으로 지워졌습니다. 🧹');
      showModal.value = false;
      router.push('/board'); // 삭제 완료 후 게시판 목록으로 이동

    } catch (error) {
      console.error("삭제 에러:", error);

      // 백엔드에서 비밀번호가 틀렸을 때 보통 400 에러를 내려줍니다.
      if (error.response && error.response.status === 400) {
        alert('비밀번호가 일치하지 않습니다! 🙅‍♂️');
      } else {
        alert('삭제에 실패했습니다. 비밀번호를 다시 확인해 주세요.');
      }
    }
  }
};

const fetchComments = async () => {
  try {
    const postId = route.params.id;
    const response = await axios.get(`${BASE_URL}/api/posts/${postId}/comments`);
    comments.value = response.data;
  } catch (error) {
    console.error('댓글 불러오기 에러:', error);
  }
};

//  댓글 등록 (POST)
const submitComment = async () => {
  // 1. 필수 입력값 검사
  if (!newCommentContent.value || !newCommentPassword.value) {
    alert('댓글 내용과 삭제용 비밀번호를 모두 입력해 주세요!');
    return;
  }

  try {
    const postId = route.params.id;

    const payload = {
      author: '익명작성자',
      content: newCommentContent.value,
      password: newCommentPassword.value
    };

    // 3. POST 요청 쏘기
    await axios.post(`${BASE_URL}/api/posts/${postId}/comments`, payload);


    // 4. 입력창 비워주기
    newCommentContent.value = '';
    newCommentPassword.value = '';
    fetchComments();

  } catch (error) {
    console.error('댓글 작성 에러:', error);
    alert('댓글 등록에 실패했습니다.');
  }
};

// 💡 댓글 삭제 함수 (DELETE)
const deleteComment = async (commentId) => {
  // 간단하게 브라우저 기본 알림창으로 비밀번호 입력받기
  const password = prompt('댓글을 삭제하시려면 비밀번호를 입력해주세요.');
  
  // 사용자가 '취소'를 누르거나 빈 값을 입력하면 함수 종료
  if (!password) {
    return;
  }

  try {
    const postId = route.params.id;

    // 백엔드로 DELETE 요청 (주소에 postId, commentId 넣고 / 쿼리로 password 전송)
    await axios.delete(`${BASE_URL}/api/posts/${postId}/comments/${commentId}`, {
      params: { password: password }
    });

    
    // 삭제가 끝났으니 댓글 목록을 다시 불러와서 화면 새로고침!
    fetchComments();

  } catch (error) {
    console.error('댓글 삭제 에러:', error);
    
    if (error.response && error.response.status === 400) {
      alert('비밀번호가 일치하지 않습니다! 🙅‍♂️');
    } else {
      alert('댓글 삭제에 실패했습니다.');
    }
  }
};

</script>

<style scoped>
.detail-view {
  max-width: 800px;
  margin: 0 auto;
}

.post-card {
  background-color: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.post-header {
  border-bottom: 2px solid #F0F8FF;
  padding-bottom: 20px;
  margin-bottom: 30px;
}

.category-badge {
  background-color: #E0F2FE;
  color: #0369A1;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 13px;
  display: inline-block;
  margin-bottom: 15px;
}

.title {
  color: #1E293B;
  margin: 0 0 15px 0;
  font-size: 24px;
}

.meta-info {
  color: #94A3B8;
  font-size: 14px;
}

.post-content {
  min-height: 200px;
  color: #334155;
  line-height: 1.8;
  font-size: 16px;
  margin-bottom: 40px;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #F1F5F9;
  padding-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 14px;
}

.btn-list {
  background-color: #F1F5F9;
  color: #64748B;
}

.right-buttons {
  display: flex;
  gap: 10px;
}

.btn-edit {
  background-color: #E0F2FE;
  color: #0369A1;
}

.btn-delete {
  background-color: #FFE4E6;
  color: #BE123C;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.password-modal {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 300px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.password-modal h3 {
  margin-top: 0;
  color: #1E293B;
}

.password-modal p {
  color: #64748B;
  font-size: 14px;
  margin-bottom: 20px;
}

.modal-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.modal-buttons button {
  flex: 1;
}

.btn-submit {
  background-color: #78C2F3;
  color: white;
}

.comments-section {
  margin-top: 40px;
  border-top: 2px dashed #E2E8F0;
  padding-top: 20px;
}

.comments-title {
  font-size: 16px;
  color: #1E293B;
  margin-bottom: 15px;
}

.comment-write-box {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.comment-pw-input {
  width: 100px;
  padding: 10px;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
}

.comment-text-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}

.comment-pw-input:focus,
.comment-text-input:focus {
  border-color: #78C2F3;
}

.btn-comment-submit {
  background-color: #78C2F3;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0 20px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.btn-comment-submit:hover {
  background-color: #0284C7;
}

/* 불러온 댓글 리스트 스타일 */
.comment-item {
  padding: 15px;
  background-color: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  margin-bottom: 10px;
  position: relative; /* 삭제 버튼 위치 기준점 */
}
.comment-info {
  font-size: 12px;
  color: #64748B;
  margin-bottom: 8px;
  display: flex;
  gap: 10px;
}
.comment-author {
  font-weight: bold;
  color: #0369A1;
}
.comment-content {
  font-size: 14px;
  color: #334155;
  line-height: 1.5;
}
.empty-comment {
  text-align: center;
  color: #94A3B8;
  padding: 30px 0;
  font-size: 14px;
}
.btn-delete-comment {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  opacity: 0.5;
  transition: 0.2s;
}
.btn-delete-comment:hover {
  opacity: 1;
  transform: scale(1.2);
}
</style>