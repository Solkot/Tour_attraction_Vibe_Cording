import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useBoardStore = defineStore('board', () => {
    const posts = ref([
        {
            id: 2,
            category: '관광지',
            title: '금오산 둘레길 지금 단풍 상태 완전 절정이에요! 🍁',
            content: '가족들과 산책 다녀오기 딱 좋은 날씨입니다. 강추해요!',
            password: '1234',
            author: '익명작성자',
            date: '2026.07.14',
            views: 142
        },
        {
            id: 1,
            category: '음식점',
            title: '송정동 복개천 고기집 추천받습니다',
            content: '회식하기 좋은 곳 어디 있을까요?',
            password: '1234',
            author: '익명작성자',
            date: '2026.07.13',
            views: 56
        }
    ])

    const nextId = ref(3)

    // 글 쓰기
    const addPost = (newPost) => {
        posts.value.unshift({
            ...newPost,
            id: nextId.value++,
            author: '익명작성자',
            date: new Date().toLocaleDateString(),
            views: 0
        })
    }

    // 특정 글 1개 가져오기
    const getPostById = (id) => {
        return posts.value.find(post => post.id === Number(id))
    }

    // ⭐️ [추가됨] 글 수정하기
    const updatePost = (id, updatedData) => {
        const index = posts.value.findIndex(p => p.id === Number(id))
        if (index !== -1) {
            posts.value[index] = { ...posts.value[index], ...updatedData }
        }
    }

    // ⭐️ [추가됨] 글 삭제하기
    const deletePost = (id) => {
        posts.value = posts.value.filter(p => p.id !== Number(id))
    }

    // 사용할 함수들 밖으로 내보내기
    return { posts, addPost, getPostById, updatePost, deletePost }
})