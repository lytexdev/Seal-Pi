import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import axios from "axios"; // axios importieren
import App from "./App.vue";
import LoginPage from "./pages/login-page.vue";
import AdminPage from "./pages/admin-page.vue";
import CameraPage from "./pages/camera-page.vue";

axios.defaults.withCredentials = true;

const routes = [
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/admin", name: "Admin", component: AdminPage },
  { path: "/camera", name: "Camera", component: CameraPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

async function checkUserStatus() {
  try {
    const response = await axios.get("/api/user-status");
    return response.data;
  } catch {
    return { is_logged_in: false, is_admin: false };
  }
}

router.beforeEach(async (to, from, next) => {
  const { is_logged_in, is_admin } = await checkUserStatus();

  if (to.path === "/login") {
    is_logged_in ? next("/") : next();
  } else if (!is_logged_in) {
    next("/login");
  } else if (to.path === "/admin" && !is_admin) {
    next("/");
  } else {
    next();
  }
});

const app = createApp(App);
app.use(router);
app.mount("#app");
