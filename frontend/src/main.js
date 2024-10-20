import { createApp } from "vue"
import { createRouter, createWebHistory } from "vue-router"
import App from "./App.vue"
import DashboardPage from "./pages/dashboard-page.vue"
import AdminPage from "./pages/admin-page.vue"
import CameraPage from "./pages/camera-page.vue"

const routes = [
  { path: "/", name: "Dashboard", component: DashboardPage },
  { path: "/admin", name: "Admin", component: AdminPage },
  { path: "/camera", name: "Camera", component: CameraPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount("#app")
