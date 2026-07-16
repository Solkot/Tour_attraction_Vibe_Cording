<template>
  <div class="home-view">
    <section class="hero-section">
      <div class="hero-content">
        <span class="badge">힐링 당일치기 여행 가이드</span>
        <h1 class="title">
          구미의 <span class="highlight">숨겨진 매력</span>을<br />
          발견해 보세요
        </h1>
        <p class="subtitle">
          아름다운 자연과 핫플이 가득한 구미.<br />
          마이구미와 함께 나만의 완벽한 하루를 설계해 보세요.
        </p>
        
        <div class="cta-buttons">
          <button class="btn-primary" @click="$router.push('/map')">
            🗺️ 지도에서 탐색하기
          </button>
          <button class="btn-secondary" @click="$router.push('/board')">
            💬 실시간 여행 꿀팁 보기
          </button>
        </div>
      </div>
      
      <div class="floating-elements">
        <div class="float-item icon-1">🏛️</div>
        <div class="float-item icon-2">🍽️</div>
        <div class="float-item icon-3">☕</div>
        <div class="float-item icon-4">📸</div>
      </div>
    </section>

    <section class="features-section">
      <div class="feature-card" @click="$router.push('/map')">
        <div class="feature-icon">📍</div>
        <h3>스마트 지도 탐색</h3>
        <p>카카오맵 기반으로 구미시 구석구석의<br/>명소와 맛집을 한눈에 찾아보세요.</p>
      </div>
      
      <div class="feature-card" @click="$router.push('/course')">
        <div class="feature-icon">🛤️</div>
        <h3>나만의 코스 설계</h3>
        <p>가고 싶은 곳을 담아 나만의 동선을 만들고,<br/> 지도 위에서 한눈에 확인하세요.</p>
      </div>
      
      <div class="feature-card" @click="$router.push('/board')">
        <div class="feature-icon">🐰</div>
        <h3>익명 커뮤니티</h3>
        <p>구미 여행의 생생한 후기와 꿀팁을 나누어 보세요.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home-view {
  width: 100%;
  min-height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-x: hidden;
}

/* 🌟 히어로 섹션 */
.hero-section {
  position: relative;
  width: 100%;
  padding: 100px 20px 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 0 0 50px 50px;
  margin-bottom: 60px;
}

.hero-content {
  z-index: 10;
  animation: fadeUp 0.8s ease-out;
}

.badge {
  display: inline-block;
  padding: 8px 16px;
  background-color: #bae6fd;
  color: #0284c7;
  font-weight: 800;
  font-size: 14px;
  border-radius: 30px;
  margin-bottom: 20px;
}

.title {
  font-size: 48px;
  font-weight: 900;
  color: #0f172a;
  line-height: 1.3;
  margin-bottom: 20px;
}

.highlight {
  color: #0369a1;
  position: relative;
}

.highlight::after {
  content: '';
  position: absolute;
  bottom: 5px;
  left: 0;
  width: 100%;
  height: 12px;
  background-color: #bae6fd;
  z-index: -1;
  border-radius: 4px;
}

.subtitle {
  font-size: 18px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 40px;
}

/* 버튼 디자인 */
.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

button {
  padding: 16px 32px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: none;
}

.btn-primary {
  background-color: #38bdf8;
  color: white;
  box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3);
}

.btn-primary:hover {
  background-color: #0284c7;
  transform: translateY(-3px);
  box-shadow: 0 15px 25px rgba(2, 132, 199, 0.3);
}

.btn-secondary {
  background-color: white;
  color: #0369a1;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover {
  background-color: #f8fafc;
  transform: translateY(-3px);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1);
}

/* 둥둥 떠다니는 아이콘들 */
.floating-elements {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.float-item {
  position: absolute;
  font-size: 40px;
  opacity: 0.6;
  animation: float 6s ease-in-out infinite;
}

.icon-1 { top: 20%; left: 15%; animation-delay: 0s; }
.icon-2 { top: 60%; left: 10%; animation-delay: 1s; }
.icon-3 { top: 30%; right: 15%; animation-delay: 2s; }
.icon-4 { top: 70%; right: 10%; animation-delay: 3s; font-size: 50px; }

@keyframes float {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 🌟 기능 소개 섹션 */
.features-section {
  display: flex;
  gap: 30px;
  max-width: 1200px;
  padding: 0 20px 80px;
  flex-wrap: wrap;
  justify-content: center;
}

.feature-card {
  flex: 1;
  min-width: 300px;
  background: white;
  padding: 40px 30px;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  border: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15);
  border-color: #bae6fd;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 15px;
}

.feature-card p {
  font-size: 15px;
  color: #64748b;
  line-height: 1.6;
  word-break: keep-all;
}

/* 모바일 대응 */
@media screen and (max-width: 768px) {
  .title { font-size: 32px; }
  .cta-buttons { flex-direction: column; }
  .features-section { flex-direction: column; }
}
</style>