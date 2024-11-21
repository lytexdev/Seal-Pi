<template>
    <section id="login">
        <Logo title="LOGIN" />
        <form class="login-form" @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username_or_email">Username or Email</label>
                <input v-model="usernameOrEmail" type="text" id="username_or_email"
                    placeholder="Enter your username or email" required />
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input v-model="password" type="password" id="password" placeholder="Enter your password" required />
            </div>

            <div v-if="mfaRequired" class="form-group">
                <label for="totp_code">TOTP Code</label>
                <input v-model="totpCode" type="text" id="totp_code" placeholder="Enter your 2-FA code" />
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
const totpCode = ref('')
const mfaRequired = ref(false)
const router = useRouter()

const handleLogin = async () => {
    try {
        const response = await axios.post('/api/login', {
            username_or_email: usernameOrEmail.value,
            password: password.value,
            totp_code: totpCode.value || null,
        })

        if (response.data.message === "Login successful") {
            const isAdmin = response.data.is_admin
            router.push(isAdmin ? '/admin' : '/')
        }
    } catch (error) {
        if (error.response?.data?.message === "TOTP code is required") {
            mfaRequired.value = true
        } else {
            alert(error.response?.data?.message || "Login failed")
        }
    }
}
</script>
