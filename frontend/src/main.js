import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router";
import App from './App.vue'
import CameraPage from './pages/camera-page.vue'

const app = createApp(App)
const routes = [
    { path: "/", name: "Camera", component: CameraPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

app.use(router)
app.mount('#app')
