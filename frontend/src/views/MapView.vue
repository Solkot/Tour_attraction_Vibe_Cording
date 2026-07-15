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
          <span class="region-tag adjacent-tag" v-for="adj in adjacentRegions" :key="adj" @click="changeCenterRegion(adj)">
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
        <p class="result-count">총 <strong>{{ placeList.length }}</strong>개의 장소를 찾았어요!</p>

        <button class="add-course-btn" @click="courseStore.addCourse(place)">
          📌 내 코스에 추가
        </button>

        <div class="place-list">
          <div class="place-card" v-for="place in placeList" :key="place.id">
            <div class="place-header">
              <span class="badge" :class="getCategoryClass(place.category)">{{ place.category }}</span>
              <span class="region-label">🚩 {{ place.region }}</span>
            </div>
            <h4 class="place-name">{{ place.name }}</h4>
            <p class="place-desc">{{ place.desc }}</p>
            <button class="add-course-btn">📌 내 코스에 추가</button>
          </div>
        </div>

        <div v-if="placeList.length === 0" class="empty-result">
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
import { ref, computed, watch} from 'vue';
import { useCourseStore } from '../stores/courseStore';
import axios from 'axios';

const courseStore = useCourseStore();

// 1. 구미시 주요 행정구역 및 인접 지역 데이터
const regionData = {
  // --- 강서 지역  ---
  '원평동': ['송정동', '도량동', '지산동', '신평동', '남통동'],
  '송정동': ['원평동', '형곡동', '광평동', '신평동'],
  '도량동': ['원평동', '봉곡동', '선기동', '지산동'],
  '형곡동': ['송정동', '사곡동', '상모동', '남통동'],
  
  // --- 강동 지역 --
  '진평동': ['인의동', '구평동', '황상동', '임수동'],
  '인의동': ['진평동', '황상동', '구평동'],
  '구평동': ['진평동', '인의동', '신동'],
  '옥계동': ['산동읍', '거의동', '구포동'],
  '산동읍': ['옥계동', '해평면', '장천면'] // 확장 단지 포함
};

const regions = Object.keys(regionData).map(name => ({ name }));

const selectedRegion = ref('');
const adjacentRegions = computed(() => {
  if (!selectedRegion.value) return [];
  return regionData[selectedRegion.value] || [];
});

const placeList = ref([]);

// 3. API 호출 함수 (선택한 지역 + 인접 지역 데이터 모두 가져오기)
const fetchPlaces = async () => {
  if (!selectedRegion.value) return;

  try {
    // 검색할 타겟 지역 목록 
    const targetRegions = [selectedRegion.value, ...adjacentRegions.value];
    
    // 각 지역마다 백엔드에 요청을 보내는 준비 
    const BASE_URL = 'http://192.168.42.82:8000';
    
    const requests = targetRegions.map(regionName => 
      axios.get(`${BASE_URL}/api/places`, { 
        params: { region: regionName } 
      })
    );

    const responses = await Promise.all(requests);
    
    placeList.value = responses.flatMap(res => res.data);
    
    console.log("데이터 받아오기 성공!", placeList.value);

  } catch (error) {
    console.error("API 호출 중 에러 발생:", error);
    alert("서버에서 장소 정보를 불러오는데 실패했습니다.");
  }
};

// 인접 지역 태그 클릭 시 중심 지역을 바꿔주는 함수
const changeCenterRegion = (newRegion) => {
  // 우리가 만든 regionData(드롭다운 목록)에 해당 동네가 키값으로 존재하는지 확인
  if (regionData[newRegion]) {
    selectedRegion.value = newRegion; 
    // 값이 바뀌면 알아서 watch가 감지해서 fetchPlaces()를 다시 실행해줍니다!
  } else {
    // 만약 데이터가 없는 동네라면 (예: 남통동, 신평동 등을 key로 추가 안 했을 경우)
    alert(`${newRegion} 데이터는 아직 준비 중입니다! 😅 (추후 업데이트 예정)`);
  }
};

// 4. 사용자가 드롭다운에서 지역을 선택할 때마다 자동으로 fetchPlaces 실행
watch(selectedRegion, () => {
  fetchPlaces();
});

// 카테고리 색상 클래스 (기존 유지)
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
  cursor: pointer; /* 👈 마우스 올리면 손가락 모양으로 바뀜 */
  transition: all 0.2s ease; /* 👈 부드러운 애니메이션 효과 */
}

/* 👈 마우스를 올렸을 때 배경색과 글자색이 반전되는 효과 추가 */
.adjacent-tag:hover {
  background-color: #78C2F3;
  color: white;
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