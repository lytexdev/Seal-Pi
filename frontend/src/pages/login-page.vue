<template>
    <section id="login">
        <Logo title="LOGIN" />
        <form class="login-form" @submit.prevent="login">
            <div class="form-group">
                <label for="username_or_email">Username or Email</label>
                <input v-model="usernameOrEmail" type="text" id="username_or_email"
                    placeholder="Enter your username or email" required />
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input v-model="password" type="password" id="password" placeholder="Enter your password" required />
            </div>
            <button type="submit" class="button button-primary">Login</button>
        </form>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Logo from '../components/Logo.vue'

const usernameOrEmail = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
    try {
        const response = await axios.post('/api/login', {
            username_or_email: usernameOrEmail.value,
            password: password.value
        })

        if (response.status === 200) {
            const isAdmin = response.data.is_admin
            router.push(isAdmin ? '/admin' : '/')
        }
    } catch (error) {
        alert(error.response?.data?.message || "Login failed")
    }
}
</script>
