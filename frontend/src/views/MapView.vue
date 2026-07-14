<template>
  <div class="map-view">
    <div class="region-selector-container">
      <div class="selector-header">
        <h2>어디를 중심으로 탐색할까요?</h2>
        <select v-model="selectedRegion" class="region-dropdown">
          <option disabled value="">구미시 행정구역 선택</option>
          <option v-for="region in regions" :key="region.name" :value="region.name">
            {{ region.name }}
          </option>
        </select>
      </div>

      <div class="adjacent-regions-display" v-if="selectedRegion">
        <h3>📍 {{ selectedRegion }} 근처 인접 지역</h3>
        <div class="tags-container">
          <span class="region-tag center-tag">{{ selectedRegion }} (중심)</span>
          <span class="region-tag adjacent-tag" v-for="adj in adjacentRegions" :key="adj">
            {{ adj }}
          </span>
        </div>
      </div>
      <div class="placeholder" v-else>
        <p>위에서 지역을 선택하시면 주변 정보를 찾아드릴게요!</p>
      </div>
    </div>

    <div class="sidebar">
      <h3 class="sidebar-title">📍 탐색 결과</h3>

      <div v-if="selectedRegion" class="list-container">
        <p class="result-count">총 <strong>{{ filteredPlaces.length }}</strong>개의 장소를 찾았어요!</p>

        <button class="add-course-btn" @click="courseStore.addCourse(place)">
          📌 내 코스에 추가
        </button>

        <div class="place-list">
          <div class="place-card" v-for="place in filteredPlaces" :key="place.id">
            <div class="place-header">
              <span class="badge" :class="getCategoryClass(place.category)">{{ place.category }}</span>
              <span class="region-label">🚩 {{ place.region }}</span>
            </div>
            <h4 class="place-name">{{ place.name }}</h4>
            <p class="place-desc">{{ place.desc }}</p>
            <button class="add-course-btn">📌 내 코스에 추가</button>
          </div>
        </div>

        <div v-if="filteredPlaces.length === 0" class="empty-result">
          <p>이 주변에는 아직 등록된 장소가 없네요 🥲</p>
        </div>
      </div>

      <div v-else class="sidebar-placeholder">
        <p>왼쪽에서 지역을 선택하시면<br>주변 명소와 맛집 리스트가 나타납니다!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '../stores/courseStore';

const courseStore = useCourseStore();

// 1. 구미시 주요 행정구역 및 인접 지역 데이터
const regionData = {
  '원평동': ['송정동', '도량동', '지산동', '신평동'],
  '송정동': ['원평동', '형곡동', '광평동'],
  '도량동': ['원평동', '봉곡동', '선기동'],
  '형곡동': ['송정동', '사곡동', '임은동']
};
const regions = Object.keys(regionData).map(name => ({ name }));

const selectedRegion = ref('');

// 선택된 지역의 인접 지역 계산
const adjacentRegions = computed(() => {
  if (!selectedRegion.value) return [];
  return regionData[selectedRegion.value] || [];
});

// 2. 가짜 장소 데이터 (★나중에 백엔드 API가 완성되면 이 배열을 갈아끼우면 됩니다!)
const allPlaces = [
  { id: 1, name: '원평동 문화의 거리', category: '관광지', region: '원평동', desc: '다양한 볼거리와 먹거리가 가득한 구미의 중심 거리.' },
  { id: 2, name: '송정동 복개천 맛집골목', category: '음식점', region: '송정동', desc: '구미 현지인들이 사랑하는 맛집이 모여있는 곳.' },
  { id: 3, name: '형곡 전망대', category: '관광지', region: '형곡동', desc: '구미 시내를 한눈에 내려다볼 수 있는 멋진 야경 명소.' },
  { id: 4, name: '도량동 빵집', category: '음식점', region: '도량동', desc: '갓 구운 빵 냄새가 가득한 동네 숨은 빵 맛집.' },
  { id: 5, name: '원평 중앙시장', category: '쇼핑', region: '원평동', desc: '정겨운 인심과 맛있는 길거리 음식이 있는 전통시장.' },
  { id: 6, name: '지산동 샛강 생태공원', category: '관광지', region: '지산동', desc: '산책하기 좋은 조용한 생태공원. 고니 서식지.' }
];

// 3. 핵심 로직: 선택한 지역 + 인접 지역에 포함되는 장소만 걸러내기
const filteredPlaces = computed(() => {
  if (!selectedRegion.value) return [];

  // 검색 대상이 될 지역 목록 생성 (예: ['원평동', '송정동', '도량동', '지산동', '신평동'])
  const targetRegions = [selectedRegion.value, ...adjacentRegions.value];

  // 전체 장소 중, region이 targetRegions 안에 속해있는 장소만 반환
  return allPlaces.filter(place => targetRegions.includes(place.region));
});

// 카테고리에 맞춰 색상 클래스를 뱉어주는 함수
const getCategoryClass = (category) => {
  if (category === '관광지') return 'category-tour';
  if (category === '음식점') return 'category-food';
  if (category === '숙소') return 'category-stay';
  if (category === '쇼핑') return 'category-shop';
  return '';
};
</script>

<style scoped>
/* 기존 스타일은 유지하고 사이드바 리스트 스타일 추가 */
.map-view {
  display: flex;
  height: 100%;
  gap: 20px;
}

.region-selector-container {
  flex: 1;
  background-color: #E2E8F0;
  border-radius: 16px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.selector-header {
  text-align: center;
  margin-bottom: 30px;
}

.region-dropdown {
  padding: 12px 20px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #CBD5E1;
  width: 300px;
  margin-top: 15px;
}

.adjacent-regions-display {
  text-align: center;
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  width: 80%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 15px;
}

.region-tag {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
}

.center-tag {
  background-color: #78C2F3;
  color: white;
}

.adjacent-tag {
  background-color: #E0F2FE;
  color: #0369A1;
  border: 1px solid #78C2F3;
}

.placeholder {
  color: #64748B;
  margin-top: 50px;
}

/* 오른쪽 사이드바 영역 */
.sidebar {
  width: 380px;
  background-color: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.sidebar-title {
  color: #1E293B;
  border-bottom: 2px solid #F0F8FF;
  padding-bottom: 10px;
  margin-top: 0;
}

.sidebar-placeholder {
  text-align: center;
  color: #94A3B8;
  margin-top: 50px;
  line-height: 1.6;
}

.result-count {
  color: #0369A1;
  font-size: 14px;
  margin-bottom: 15px;
}

/* 장소 리스트 스크롤 영역 */
.list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.place-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 5px;
}

/* 스크롤바 예쁘게 */
.place-list::-webkit-scrollbar {
  width: 6px;
}

.place-list::-webkit-scrollbar-thumb {
  background-color: #CBD5E1;
  border-radius: 4px;
}

/* 장소 카드 디자인 */
.place-card {
  background-color: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
}

.place-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.region-label {
  font-size: 12px;
  color: #64748B;
  font-weight: bold;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.category-tour {
  background-color: #10B981;
}

.category-food {
  background-color: #F59E0B;
}

.category-stay {
  background-color: #3B82F6;
}

.category-shop {
  background-color: #8B5CF6;
}

.place-name {
  margin: 0 0 8px 0;
  color: #1E293B;
  font-size: 16px;
}

.place-desc {
  color: #64748B;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 15px;
}

.add-course-btn {
  width: 100%;
  padding: 10px;
  background-color: white;
  color: #78C2F3;
  border: 2px solid #78C2F3;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.add-course-btn:hover {
  background-color: #78C2F3;
  color: white;
}

.empty-result {
  text-align: center;
  color: #94A3B8;
  padding: 40px 0;
}
</style>