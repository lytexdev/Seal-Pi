<template>
    <div class="logo flex">
        <img class="logo-image" :src="logoUrl" alt="Seal-Pi" height="64px" width="64px">
        <h1>{{ title }}</h1>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    title: String
})
const logoUrl = './static/logo.svg'
</script>
