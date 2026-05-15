import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'
import App from './App.vue'
import './style.css'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

// 初始化用户状态
import { useUserStore } from './stores/user'
const userStore = useUserStore()
userStore.initFromStorage()

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus, {
  color: '#1890FF'
})
app.use(router)

app.mount('#app')