<template>
    <section id="dashboard">
        <Logo title="Dashboard" />

        <div class="dashboard-greeting">
            <b>Hello, lytex!</b>
        </div>

        <nav class="nav-main">
            <div class="nav-link">
                <router-link to="/camera">Security Camera</router-link>
                <router-link to="/frp">Fast Reverse Proxy</router-link>
            </div>
        </nav>
    </section>
</template>

<script setup>
import Logo from '../components/Logo.vue'
</script>