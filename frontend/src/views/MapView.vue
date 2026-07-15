<template>
  <div class="map-view">
    <section class="region-selector-container">
      <div class="selector-header">
        <h2>어디를 중심으로 탐색할까요?</h2>

        <select v-model="selectedRegion" class="region-dropdown">
          <option disabled value="">구미시 행정구역 선택</option>
          <option v-for="region in regions" :key="region.name" :value="region.name">
            {{ region.name }}
          </option>
        </select>
      </div>

      <div v-if="selectedRegion" class="adjacent-regions-display">
        <h3>📍 {{ selectedRegion }} 근처 인접 지역</h3>

        <div class="tags-container">
          <span class="region-tag center-tag">
            {{ selectedRegion }} (중심)
          </span>

          <button v-for="adj in adjacentRegions" :key="adj" type="button" class="region-tag adjacent-tag"
            @click="changeCenterRegion(adj)">
            {{ adj }}
          </button>
        </div>
      </div>

      <div id="map" class="kakao-map"></div>
    </section>

    <aside class="sidebar">
      <h3 class="sidebar-title">📍 탐색 결과</h3>

      <div v-if="selectedRegion" class="list-container">
        <p class="result-count">
          총 <strong>{{ placeList.length }}</strong>개의 장소를 찾았어요!
        </p>

        <div v-if="placeList.length > 0" class="place-list">
          <article v-for="(place, index) in placeList" :key="index" class="place-card">
            <div class="place-header">
              <span class="badge" :class="getCategoryClass(place.category)">
                {{ place.category }}
              </span>

              <span class="region-label">🚩 {{ place.region }}</span>
            </div>

            <h4 class="place-name">{{ place.name }}</h4>
            <p class="place-desc">{{ place.desc }}</p>

            <button type="button" class="add-course-btn" @click="courseStore.addCourse(place)">
              📌 내 코스에 추가
            </button>
          </article>
        </div>

        <div v-else class="empty-result">
          <p>이 주변에는 아직 등록된 장소가 없네요 🥲</p>
        </div>
      </div>

      <div v-else class="sidebar-placeholder">
        <p>
          왼쪽에서 지역을 선택하시면<br />
          주변 명소와 맛집 리스트가 나타납니다!
        </p>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { onMounted } from 'vue';
import axios from 'axios';
import { useCourseStore } from '../stores/courseStore';

const courseStore = useCourseStore();

const regionData = {
  // 강서 지역
  원평동: ['송정동', '도량동', '지산동', '신평동', '남통동'],
  송정동: ['원평동', '형곡동', '광평동', '신평동'],
  도량동: ['원평동', '봉곡동', '선기동', '지산동'],
  형곡동: ['송정동', '사곡동', '상모동', '남통동'],

  // 강동 지역
  진평동: ['인의동', '구평동', '황상동', '임수동'],
  인의동: ['진평동', '황상동', '구평동'],
  구평동: ['진평동', '인의동', '신동'],
  옥계동: ['산동읍', '거의동', '구포동'],
  산동읍: ['옥계동', '해평면', '장천면'],
};

const regions = Object.keys(regionData).map((name) => ({ name }));

const selectedRegion = ref('');
const placeList = ref([]);

const adjacentRegions = computed(() => {
  if (!selectedRegion.value) return [];
  return regionData[selectedRegion.value] || [];
});

const fetchPlaces = async () => {
  if (!selectedRegion.value) {
    placeList.value = [];
    return;
  }

  try {
    const targetRegions = [
      selectedRegion.value,
      ...adjacentRegions.value,
    ];

    const BASE_URL = 'http://192.168.42.82:8000';

    const requests = targetRegions.map((regionName) =>
      axios.get(`${BASE_URL}/api/places`, {
        params: { region: regionName },
      }),
    );

    const responses = await Promise.all(requests);
    placeList.value = responses.flatMap((response) => response.data);

    console.log('데이터 받아오기 성공!', placeList.value);
  } catch (error) {
    console.error('API 호출 중 에러 발생:', error);
    placeList.value = [];
    alert('서버에서 장소 정보를 불러오는데 실패했습니다.');
  }
};

const changeCenterRegion = (newRegion) => {
  if (regionData[newRegion]) {
    selectedRegion.value = newRegion;
    return;
  }

  alert(`${newRegion} 데이터는 아직 준비 중입니다! 😅 (추후 업데이트 예정)`);
};

watch(selectedRegion, fetchPlaces);

const getCategoryClass = (category) => {
  if (category === '관광지') return 'category-tour';
  if (category === '음식점') return 'category-food';
  if (category === '숙소') return 'category-stay';
  if (category === '쇼핑') return 'category-shop';
  return 'category-default';
};

let mapInstance = null;
let markers = [];

// 🗺️ 카카오맵 초기화 함수
const initMap = () => {
  const container = document.getElementById('map');
  if (!container) return;

  if (!window.kakao || !window.kakao.maps) {
    setTimeout(initMap, 500);
    return;
  }

  window.kakao.maps.load(() => {
    const options = {
      center: new window.kakao.maps.LatLng(36.119485, 128.344573), // 구미시청
      level: 5 
    };
    
    // 지도를 만들고 mapInstance 변수에 저장!
    mapInstance = new window.kakao.maps.Map(container, options);
    console.log('✨ 카카오맵 렌더링 완료!');

    // 지도가 만들어졌을 때 이미 데이터가 있다면 마커 바로 그리기
    if (placeList.value.length > 0) {
      displayMarkers(placeList.value);
    }
  });
};

// 📍 마커를 그려주는 마법의 함수 (새로 추가)
const displayMarkers = (places) => {
  if (!mapInstance) return;

  // 1. 기존에 꽂혀있던 마커들 싹 지우기 (새 지역 선택 시 리셋)
  markers.forEach(marker => marker.setMap(null));
  markers = [];

  if (places.length === 0) return;

  // 2. 마커들이 모두 보이게 지도를 조절할 '영역 객체' 생성
  const bounds = new window.kakao.maps.LatLngBounds();

  // 3. 장소 리스트를 돌면서 하나씩 마커 찍기
  places.forEach(place => {
    // ⚠️ 주의: 백엔드에서 위도(lat), 경도(lng) 값을 준다고 가정했습니다!
    // 만약 변수명이 다르면 (예: latitude, longitude) 그에 맞게 수정해주세요.
    const position = new window.kakao.maps.LatLng(place.lat, place.lng);

    const marker = new window.kakao.maps.Marker({
      map: mapInstance,
      position: position,
      title: place.name // 마우스 올리면 장소 이름이 뜹니다!
    });

    markers.push(marker); // 나중에 지우기 위해 배열에 저장
    bounds.extend(position); // 마커의 위치를 영역 객체에 포함
  });

  // 4. 모든 마커가 한눈에 들어오도록 지도 중심과 줌 레벨 자동 조절!
  mapInstance.setBounds(bounds);
};

// 💡 백엔드에서 장소 데이터를 새로 받아올 때마다 자동으로 마커 그리기!
watch(placeList, (newPlaces) => {
  displayMarkers(newPlaces);
});

onMounted(() => {
  initMap();
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.map-view {
  display: flex;
  width: 100%;
  height: 80vh;
  min-height: 620px;
  max-width: 2200px;
  gap: 25px;
  padding: 10px;
}

.region-selector-container {
  flex: 6;
  min-width: 0;
  display: flex;
  padding-top: 50px;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background: linear-gradient(145deg, #f0f8ff, #e0f2fe);
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(120, 194, 243, 0.1);
}

.selector-header {
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.selector-header h2 {
  margin: 0 0 5px;
  color: #0369a1;
  font-size: 26px;
  font-weight: 800;
}

.region-dropdown {
  width: 100%;
  margin-top: 15px;
  padding: 15px 20px;
  color: #1e293b;
  font-size: 16px;
  background-color: #ffffff;
  border: 2px solid #bae6fd;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.region-dropdown:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
}

.adjacent-regions-display {
  width: 100%;
  max-width: 550px;
  margin-top: 40px;
  padding: 35px 25px;
  text-align: center;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
  transition: transform 0.3s ease;
}

.adjacent-regions-display:hover {
  transform: translateY(-2px);
}

.adjacent-regions-display h3 {
  margin: 0 0 15px;
  color: #0284c7;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.region-tag {
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.3px;
  border-radius: 25px;
}

.center-tag {
  color: #ffffff;
  background-color: #38bdf8;
  box-shadow: 0 4px 10px rgba(56, 189, 248, 0.3);
}

.adjacent-tag {
  color: #0369a1;
  font-family: inherit;
  background-color: #ffffff;
  border: 1px solid #78c2f3;
  cursor: pointer;
  transition: all 0.25s ease;
}

.adjacent-tag:hover {
  color: #ffffff;
  background-color: #78c2f3;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(120, 194, 243, 0.3);
}

.placeholder {
  margin-top: 50px;
  padding: 15px 30px;
  color: #64748b;
  font-size: 16px;
  text-align: center;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 20px;
}

.placeholder p {
  margin: 0;
}

/* 오른쪽 탐색 결과 영역 */
.sidebar {
  flex: 4;
  min-width: 0;
  min-height: 0;
  padding: 25px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #ffffff;
  border: 1px solid #e0f2fe;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(120, 194, 243, 0.08);
}

.sidebar-title {
  flex-shrink: 0;
  margin: 0 0 18px;
  padding-bottom: 15px;
  color: #0369a1;
  font-size: 20px;
  border-bottom: 2px dashed #bae6fd;
}

.list-container {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.result-count {
  flex-shrink: 0;
  margin: 0 0 14px;
  padding: 11px 12px;
  color: #0284c7;
  font-size: 15px;
  text-align: center;
  background-color: #f0f9ff;
  border-radius: 10px;
}

.place-list {
  flex: 1;
  min-height: 0;
  padding: 2px 8px 8px 2px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.place-list::-webkit-scrollbar {
  width: 8px;
}

.place-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.place-list::-webkit-scrollbar-thumb {
  background-color: #bae6fd;
  border-radius: 10px;
}

.place-list::-webkit-scrollbar-thumb:hover {
  background-color: #78c2f3;
}

.place-card {
  flex-shrink: 0;
  padding: 18px;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  border: 1px solid #e0f2fe;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.025);
  transition: transform 0.2s ease, border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.place-card:hover {
  border-color: #78c2f3;
  transform: translateY(-3px);
  box-shadow: 0 10px 18px rgba(120, 194, 243, 0.15);
}

.place-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.region-label {
  padding: 4px 8px;
  color: #0284c7;
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
  background-color: #f0f9ff;
  border-radius: 6px;
}

.badge {
  padding: 6px 10px;
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.5px;
  border-radius: 8px;
}

.category-tour {
  background-color: #34d399;
}

.category-food {
  background-color: #fbbf24;
}

.category-stay {
  background-color: #60a5fa;
}

.category-shop {
  background-color: #a78bfa;
}

.category-default {
  background-color: #94a3b8;
}

.place-name {
  margin: 0 0 8px;
  color: #0f172a;
  font-size: 18px;
  font-weight: 800;
  line-height: 1.35;
}

.place-desc {
  margin: 0 0 16px;
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  word-break: keep-all;
}

.add-course-btn {
  width: auto;
  min-width: 140px;
  margin-top: auto;
  padding: 10px 14px;
  align-self: flex-end;
  color: #0284c7;
  font-family: inherit;
  font-size: 14px;
  font-weight: 800;
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-course-btn:hover {
  color: #ffffff;
  background-color: #38bdf8;
  border-color: #38bdf8;
  transform: translateY(-1px);
}

.empty-result,
.sidebar-placeholder {
  flex: 1;
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 15px;
  line-height: 1.8;
  text-align: center;
  background-color: #f8fafc;
  border-radius: 14px;
}

.empty-result p,
.sidebar-placeholder p {
  margin: 0;
}

@media screen and (max-width: 900px) {
  .map-view {
    height: auto;
    min-height: 0;
    flex-direction: column;
  }

  .region-selector-container {
    padding: 30px 20px;
  }

  .sidebar {
    width: 100%;
    height: 600px;
  }
}

@media screen and (max-width: 520px) {
  .map-view {
    gap: 16px;
    padding: 6px;
  }

  .selector-header h2 {
    font-size: 22px;
  }

  .adjacent-regions-display {
    padding: 26px 18px;
  }

  .sidebar {
    height: 560px;
    padding: 20px 16px;
  }

  .place-header {
    align-items: flex-start;
  }

  .add-course-btn {
    width: 100%;
    align-self: stretch;
  }
}

/* 🌟 카카오맵 영역 디자인 */
.kakao-map {
  width: 100%;
  flex: 1;
  /* 남는 세로 공간을 꽉 채우도록! */
  min-height: 400px;
  margin-top: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  border: 2px solid #FFFFFF;
}
</style>
