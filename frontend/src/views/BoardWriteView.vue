<template>
  <div class="write-view">
    <div class="header">
      <h2>✍️ 새 글 쓰기</h2>
      <p>구미 여행 꿀팁을 익명으로 자유롭게 남겨주세요.</p>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label>카테고리</label>
        <select class="form-input" v-model="newPost.category">
          <option value="관광지">🏛️ 관광지</option>
          <option value="음식점">🍽️ 음식점</option>
          <option value="숙소">⛺ 숙소</option>
          <option value="쇼핑">🛒 쇼핑</option>
        </select>
      </div>

      <div class="form-group">
        <label>제목</label>
        <input type="text" class="form-input" v-model="newPost.title" placeholder="게시글 제목을 입력하세요" />
      </div>

      <div class="form-group">
        <label>수정용 비밀번호 (필수)</label>
        <input type="password" class="form-input" v-model="newPost.password" placeholder="수정/삭제 시 사용할 비밀번호 (숫자 4자리 권장)" />
        <small class="help-text">※ 비밀번호를 분실하면 글을 수정하거나 삭제할 수 없습니다.</small>
      </div>

      <div class="form-group">
        <label>내용</label>
        <textarea class="form-input textarea" rows="10" v-model="newPost.content" placeholder="내용을 입력하세요"></textarea>
      </div>

      <div class="button-group">
        <button class="btn-cancel" @click="$router.push('/board')">취소</button>
        <button class="btn-submit" @click="submitPost">등록하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// 사용자가 입력할 폼 데이터
const newPost = ref({
  category: '관광지',
  title: '',
  password: '',
  content: ''
})

// 게시글 등록 함수 (async/await로 서버 통신 처리)
const submitPost = async () => {
  // 1. 필수 입력값 검사
  if (!newPost.value.title || !newPost.value.password || !newPost.value.content) {
    alert('제목, 비밀번호, 내용을 모두 입력해 주세요!')
    return
  }
  
  try {
    const BASE_URL = 'http://192.168.42.82:8000' 
    
    const payload = {
      title: newPost.value.title,
      content: newPost.value.content,
      category: newPost.value.category,
      password: newPost.value.password
    }
    
    const response = await axios.post(`${BASE_URL}/api/posts`, payload)
    
    console.log('✅ 글쓰기 성공! 서버 응답:', response.data)
    alert('게시글이 성공적으로 등록되었습니다!')
    
    router.push('/board')
    
  } catch (error) {
    console.error('❌ 글쓰기 에러 발생:', error)
    // 에러 종류에 따라 알림창 띄우기
    if (error.response && error.response.status === 422) {
      alert('입력하신 데이터 형식이 맞지 않습니다. (Validation Error)')
    } else {
      alert('서버와 통신하는 중 문제가 발생했습니다.')
    }
  }
}
</script>

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