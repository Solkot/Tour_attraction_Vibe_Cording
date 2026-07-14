<template>
  <div class="app-container">
    <header class="gnb">
      <div class="logo">MyGumi</div>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">탐색(지도)</router-link>
        <router-link to="/board" class="nav-item">익명 게시판</router-link>
        <router-link to="/course" class="nav-item">마이 코스</router-link>
      </nav>
      <div class="profile-icon">👤</div>
    </header>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <button class="chatbot-btn">AI</button>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #F0F8FF; /* Alice Blue 배경 */
  font-family: 'sans-serif';
}

.gnb {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  height: 70px;
  background-color: #D0E7FF;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
  height: calc(100vh - 70px); /* 전체 높이에서 GNB 높이 제외 */
  padding: 20px;
  box-sizing: border-box;
}

.chatbot-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #78C2F3; /* 파스텔 하늘색 */
  color: white;
  border: none;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(120, 194, 243, 0.4);
  cursor: pointer;
  transition: transform 0.2s;
}

.chatbot-btn:hover {
  transform: scale(1.1);
}
</style>