<template>
  <div class="app-container">
    <header class="gnb">
      <div class="logo">MyGumi</div>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">탐색(지도)</router-link>
        <router-link to="/board" class="nav-item">익명 게시판</router-link>
        <router-link to="/course" class="nav-item">마이 코스</router-link>
      </nav>
      <div class="profile-icon">🐰</div>
    </header>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <div class="chat-window" v-if="isChatOpen">
      <div class="chat-header">
        <div class="ai-profile">
          <span class="ai-icon">💬</span>
          <div>
            <strong>AI Guide</strong>
            <div class="online-status">🟢 Online</div>
          </div>
        </div>
        <button class="close-btn" @click="toggleChat">✖</button>
      </div>

      <div class="chat-body" ref="chatBody">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role + '-message']">
          {{ msg.text }}
        </div>
        <div v-if="loading" class="message ai-message">답변을 생각 중입니다...</div>
      </div>

      <div class="chat-input-area">
        <input 
          type="text" 
          v-model="userQuery" 
          @keyup.enter="sendMessage"
          placeholder="마이구미에게 무엇이든 물어보세요..." 
          class="chat-input" 
        />
        <button class="send-btn" @click="sendMessage">전송</button>
      </div>
    </div>

    <button class="chatbot-btn" @click="toggleChat">
      {{ isChatOpen ? '✖' : '💬' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';

// 상태 관리
const isChatOpen = ref(false);
const userQuery = ref('');
const loading = ref(false);
const chatBody = ref(null);
const lat = ref(36.1195); // 기본값: 구미
const lon = ref(128.3444);

const messages = ref([
  { role: 'ai', text: '안녕하세요! 구미 여행 가이드입니다. 무엇을 도와드릴까요?' }
]);

// 위치 정보 가져오기
const getDeviceLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        lat.value = position.coords.latitude;
        lon.value = position.coords.longitude;
      },
      () => { console.warn("위치 정보 접근이 거부되었습니다."); }
    );
  }
};

onMounted(() => {
  getDeviceLocation();
});

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
};

const BASE_URL = import.meta.env.VITE_API_BASE_URL;
// 서버와 통신하는 함수
const sendMessage = async () => {
  if (!userQuery.value.trim()) return;

  const query = userQuery.value;
  messages.value.push({ role: 'user', text: query });
  userQuery.value = '';
  loading.value = true;

  try {
    // 🟢 수정된 Vue 코드
  const response = await fetch(`${BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_query: query,
      // 소수점 아래 4자리까지만 남기고 숫자로 변환하여 전송
      lat: parseFloat(Number(lat.value).toFixed(4)),
      lon: parseFloat(Number(lon.value).toFixed(4)),
      radius_km: 2.0,
      limit: 10
    })
  });

    const data = await response.json();
    messages.value.push({ role: 'ai', text: data.reply });
  } catch (error) {
    messages.value.push({ role: 'ai', text: '서버와 연결할 수 없습니다.' });
  } finally {
    loading.value = false;
    // 메시지 추가 후 스크롤 아래로 내리기
    await nextTick();
    if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight;
  }
};
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
}

/* 기존 스타일은 그대로 유지하시고, 아래 메시지 스타일만 추가하세요 */
.user-message {
  background-color: #78C2F3;
  color: white;
  margin-left: auto; /* 오른쪽 정렬 */
  border-top-right-radius: 0;
}
.ai-message {
  background-color: white;
  border: 1px solid #E2E8F0;
  color: #334155;
  border-top-left-radius: 0;
}

.app-container {
  width: 100%;
  max-width: 2200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #F0F8FF;
}

.gnb {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  height: 70px;
  background-color: #D0E7FF;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #0369A1;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-item {
  text-decoration: none;
  color: #1E293B;
  font-size: 16px;
  font-weight: 500;
}

.nav-item.router-link-active {
  color: #0284C7;
  font-weight: bold;
  border-bottom: 3px solid #0284C7;
  padding-bottom: 5px;
}

.profile-icon {
  font-size: 24px;
}

.main-content {
  height: calc(100vh - 70px);
  padding: 20px;
  box-sizing: border-box;
}

/* 플로팅 버튼 스타일 */
.chatbot-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #78C2F3;
  color: white;
  border: none;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(120, 194, 243, 0.4);
  cursor: pointer;
  transition: transform 0.2s;
  z-index: 999;
}

.chatbot-btn:hover {
  transform: scale(1.1);
}

/* 챗봇 창 스타일 */
.chat-window {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 320px;
  height: 450px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1000;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-header {
  background-color: #78C2F3;
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ai-icon {
  font-size: 24px;
  background-color: white;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.online-status {
  font-size: 11px;
  font-weight: bold;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
}

.chat-body {
  flex: 1;
  padding: 15px;
  background-color: #F8FAFC;
  overflow-y: auto;
}

.message {
  padding: 12px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 10px;
  max-width: 85%;
}

.ai-message {
  background-color: white;
  border: 1px solid #E2E8F0;
  color: #334155;
  border-top-left-radius: 0;
}

.chat-input-area {
  padding: 15px;
  background-color: white;
  border-top: 1px solid #E2E8F0;
  display: flex;
  gap: 10px;
}

.chat-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #CBD5E1;
  border-radius: 20px;
  font-size: 13px;
  outline: none;
}

.chat-input:focus {
  border-color: #78C2F3;
}

.send-btn {
  background-color: #78C2F3;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0 15px;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
}
</style>