import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCourseStore = defineStore('course', () => {
    // 1. 코스에 담긴 장소들을 저장할 배열
    const courseList = ref([])

    // 2. 장소 담기 함수 (중복 체크 포함)
    const addCourse = (place) => {
        // 이미 담긴 장소인지 id로 확인
        const isExist = courseList.value.find(item => item.id === place.id)
        if (isExist) {
            alert('이미 코스에 담긴 장소입니다! 😅')
            return
        }
        courseList.value.push(place)
        alert(`'${place.name}'이(가) 내 코스에 추가되었습니다! 📍`)
    }

    // 3. 장소 빼기 (삭제) 함수
    const removeCourse = (id) => {
        courseList.value = courseList.value.filter(item => item.id !== id)
    }

    // 4. 전체 초기화 함수
    const clearCourse = () => {
        if (confirm('담아둔 코스를 모두 지우시겠습니까?')) {
            courseList.value = []
        }
    }

    // 5. 총 담긴 갯수 계산
    const totalCount = computed(() => courseList.value.length)

    return { courseList, addCourse, removeCourse, clearCourse, totalCount }
})