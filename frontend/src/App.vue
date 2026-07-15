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

      <div class="chat-body">
        <div class="message ai-message">
          안녕하세요! 구미 여행 가이드입니다. 관광지, 맛집, 교통편 등 현지에 대해 무엇이든 물어보세요!
        </div>
      </div>

      <div class="chat-input-area">
        <input type="text" placeholder="마이구미에게 무엇이든 물어보세요..." class="chat-input" />
        <button class="send-btn">전송</button>
      </div>
    </div>

    <button class="chatbot-btn" @click="toggleChat">
      {{ isChatOpen ? '✖' : '💬' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 챗봇 창 열림/닫힘 상태
const isChatOpen = ref(false);

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
};
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
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