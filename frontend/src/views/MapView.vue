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
       <div class="sidebar-placeholder">
          <h3>검색 결과</h3>
          <p v-if="selectedRegion">
            {{ selectedRegion }} 및 인접 지역의<br>
            관광지, 맛집을 불러오는 중...
          </p>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 1. 구미시 주요 행정구역 및 인접 지역 데이터 매핑 (하드코딩 또는 별도 JSON 파일로 분리 추천)
const regionData = {
  '원평동': ['송정동', '도량동', '지산동', '신평동'],
  '송정동': ['원평동', '형곡동', '광평동'],
  '도량동': ['원평동', '봉곡동', '선기동'],
  '형곡동': ['송정동', '사곡동', '임은동'],
  // ... 팀원들과 구미시 지도를 보며 데이터를 채워넣으세요!
};

const regions = Object.keys(regionData).map(name => ({ name }));

// 2. 사용자가 선택한 지역을 저장하는 반응형 변수
const selectedRegion = ref('');

// 3. 선택된 지역에 따라 인접 지역 목록을 계산하는 Computed 속성
const adjacentRegions = computed(() => {
  if (!selectedRegion.value) return [];
  return regionData[selectedRegion.value] || [];
});

</script>

<style scoped>
.map-view {
  display: flex;
  height: 100%;
  gap: 20px;
}

.region-selector-container {
  flex: 1;
  background-color: #E2E8F0; /* 또는 #F0F8FF */
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
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
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

.sidebar {
  width: 350px;
  background-color: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  padding: 20px;
}
</style>