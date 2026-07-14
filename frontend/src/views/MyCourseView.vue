<template>
  <div class="course-view">
    <div class="course-header">
      <h2>🗺️ 나의 구미 당일치기 힐링 여행 코스</h2>
      <p>내가 찜한 명소와 맛집들을 한눈에 확인하세요!</p>
    </div>

    <div class="course-layout">
      <div class="timeline-section card">
        <h3 class="section-title">📍 코스 타임라인 순서</h3>

        <div class="timeline" v-if="courseStore.totalCount > 0">
          <div class="timeline-item" v-for="(place, index) in courseStore.courseList" :key="place.id">
            <div class="node">{{ index + 1 }}</div>
            <div class="content">
              <h4>{{ place.name }} <span class="tag">{{ place.category }}</span></h4>
              <p>🚩 {{ place.region }} | {{ place.desc }}</p>
            </div>
            <button class="delete-btn" @click="courseStore.removeCourse(place.id)">❌</button>
          </div>
        </div>

        <div v-else style="padding: 40px 0; text-align: center; color: #94A3B8;">
          아직 코스에 담긴 장소가 없습니다.<br>탐색 화면에서 가고 싶은 곳을 추가해 보세요!
        </div>

        <div class="course-actions" v-if="courseStore.totalCount > 0">
          <button class="action-btn share-btn" @click="alert('코스 공유 기능은 준비 중입니다!')">💻 코스 공유하기</button>
          <button class="action-btn delete-all-btn" @click="courseStore.clearCourse">🗑️ 전체 초기화</button>
        </div>
      </div>

      <div class="preview-section card">
        <h3 class="section-title">🗺️ 코스 요약</h3>
        <div class="preview-box">
          <div class="empty-state">
            <p>총 <strong style="font-size: 24px; color:#0369A1;">{{ courseStore.totalCount }}</strong>개의 장소가</p>
            <p>코스에 담겨 있습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCourseStore } from '../stores/courseStore';
const courseStore = useCourseStore();
</script>

<style scoped>
/* 기존 스타일 그대로 복붙! */
.course-view {
  max-width: 1000px;
  margin: 0 auto;
}

.course-header {
  margin-bottom: 20px;
}

.course-header h2 {
  color: #1E293B;
  margin-bottom: 5px;
}

.course-header p {
  color: #64748B;
  margin: 0;
}

.course-layout {
  display: flex;
  gap: 20px;
}

.card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
}

.section-title {
  color: #1E293B;
  margin-top: 0;
  margin-bottom: 20px;
  border-bottom: 2px solid #F0F8FF;
  padding-bottom: 10px;
}

.timeline-section {
  flex: 6;
}

.preview-section {
  flex: 4;
}

.timeline {
  position: relative;
  padding-left: 20px;
  border-left: 2px dashed #78C2F3;
  margin-left: 15px;
}

.timeline-item {
  position: relative;
  margin-bottom: 25px;
  display: flex;
  align-items: flex-start;
}

.node {
  position: absolute;
  left: -33px;
  width: 24px;
  height: 24px;
  background-color: #78C2F3;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-weight: bold;
}

.content {
  flex: 1;
  background-color: #F8FAFC;
  padding: 15px;
  border-radius: 8px;
}

.content h4 {
  margin: 0 0 5px 0;
  color: #1E293B;
}

.tag {
  font-size: 11px;
  background-color: white;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #E2E8F0;
  margin-left: 5px;
}

.content p {
  margin: 0;
  font-size: 13px;
  color: #64748B;
}

.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  margin-top: 15px;
  transition: 0.2s;
}

.delete-btn:hover {
  transform: scale(1.2);
}

.course-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.action-btn {
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.share-btn {
  background-color: #78C2F3;
  color: white;
}

.delete-all-btn {
  background-color: #FEE2E2;
  color: #991B1B;
}

.preview-box {
  height: 300px;
  background-color: #E8F4F8;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.empty-state {
  color: #0369A1;
  font-weight: bold;
}
</style>