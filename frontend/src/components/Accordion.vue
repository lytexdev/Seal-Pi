<template>
    <section class="accordion-section">
        <div class="section-header" @click="toggleSection">
            <h2>{{ title }}</h2>
            <div class="toggle-button">
                <img src="../assets/open-folder.svg" alt="Hide" v-if="isOpen" height="36px" width="36px">
                <img src="../assets/close-folder.svg" alt="Show" v-else height="32px" width="32px">
            </div>
        </div>
        <div v-if="isOpen" class="section-content">
            <slot></slot>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    defaultOpen: {
        type: Boolean,
        default: true
    }
})

const isOpen = ref(props.defaultOpen)

const toggleSection = () => {
    isOpen.value = !isOpen.value
}
</script>
