import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'

const app = createApp(App)

app.use(createPinia()) // Pinia (상태 관리) 등록
app.use(router)        // Vue Router (페이지 이동) 등록

app.mount('#app')