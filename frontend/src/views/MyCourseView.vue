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
        <h3 class="section-title">🗺️ 코스 동선 미리보기</h3>
        
        <div id="course-map" class="preview-box">
          <div v-if="courseStore.totalCount === 0" class="empty-map-overlay">
            <p>장소를 추가하시면</p>
            <p>여기에 여행 동선이 나타납니다!</p>
          </div>
        </div>

        <div class="summary-text">
          <p>총 <strong style="font-size: 20px; color:#0369A1;">{{ courseStore.totalCount }}</strong>개의 장소가 코스에 담겨 있습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useCourseStore } from '../stores/courseStore';

const courseStore = useCourseStore();

let mapInstance = null;
let markers = [];   // 마커들을 담을 배열
let polyline = null; // 동선(선) 객체

// 🗺️ 1. 지도 초기화 함수
const initMap = () => {
  const container = document.getElementById('course-map');
  if (!container) return;

  // 카카오맵 스크립트 로드 대기 (탐색 화면과 같은 원리)
  if (!window.kakao || !window.kakao.maps) {
    setTimeout(initMap, 500);
    return;
  }

  window.kakao.maps.load(() => {
    const options = {
      center: new window.kakao.maps.LatLng(36.119485, 128.344573), // 기본 구미시청
      level: 6
    };
    mapInstance = new window.kakao.maps.Map(container, options);

    // 처음에 이미 담긴 코스가 있다면 동선 그리기
    if (courseStore.courseList.length > 0) {
      drawCourse(courseStore.courseList);
    }
  });
};

// 📍 2. 마커와 동선을 그려주는 함수
const drawCourse = (places) => {
  if (!mapInstance) return;

  // 기존에 그려진 마커와 선 지우기 (초기화)
  markers.forEach(marker => marker.setMap(null));
  markers = [];
  if (polyline) {
    polyline.setMap(null);
  }

  // 장소가 없으면 함수 종료
  if (places.length === 0) return;

  const bounds = new window.kakao.maps.LatLngBounds(); // 한눈에 보이게 할 영역
  const linePath = []; // 선을 연결할 좌표들

  places.forEach((place, index) => {
    // 🚨 백엔드 데이터에 lat, lng (위도, 경도) 값이 있다고 가정!
    const position = new window.kakao.maps.LatLng(place.lat, place.lng);
    
    // 선 경로에 좌표 추가
    linePath.push(position);
    bounds.extend(position); // 화면 영역에 좌표 포함

    // 마커 생성
    const marker = new window.kakao.maps.Marker({
      map: mapInstance,
      position: position,
      title: `${index + 1}. ${place.name}` // 마우스 올리면 순서와 이름 표시
    });
    markers.push(marker);
  });

  // 〰️ 선(Polyline) 생성 및 지도에 표시
  polyline = new window.kakao.maps.Polyline({
    path: linePath, // 연결할 좌표 배열
    strokeWeight: 4, // 선 두께
    strokeColor: '#38BDF8', // 예쁜 파란색
    strokeOpacity: 0.8, // 불투명도
    strokeStyle: 'solid' // 선 스타일 (solid, shortdash 등)
  });
  polyline.setMap(mapInstance);

  // 🔍 모든 마커가 보이도록 지도 화면 이동 및 확대/축소 자동 조절!
  mapInstance.setBounds(bounds);
};

// 💡 3. 코스 목록이 변할 때마다 자동으로 다시 그리기
watch(() => courseStore.courseList, (newList) => {
  drawCourse(newList);
}, { deep: true });

onMounted(() => {
  initMap();
});
</script>

<style scoped>
/* 기존 스타일 그대로 복붙! */
.course-view {
  max-width: 1600px;
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

/* 🌟 추가 & 수정된 스타일 */
.preview-box {
  height: 450px; /* 지도가 시원하게 보이도록 높이 키움 */
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  border: 1px solid #E2E8F0;
}

.empty-map-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(248, 250, 252, 0.9); /* 반투명 배경 */
  z-index: 10;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-weight: 800;
  font-size: 16px;
  color: #94A3B8;
  text-align: center;
}

.summary-text {
  margin-top: 15px;
  text-align: center;
  color: #64748B;
  background-color: #F0F9FF;
  padding: 15px;
  border-radius: 12px;
}
.summary-text p { margin: 0; }

.empty-state {
  color: #0369A1;
  font-weight: bold;
}
</style>