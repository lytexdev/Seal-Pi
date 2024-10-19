<template>
    <section id="liveCamera">
        <Logo title="LIVE CAMERA" />

        <div class="camera-feed">
            <img :src="cameraFeedUrl" alt="Live Camera">
        </div>
    </section>
</template>

<script setup>
import Logo from '../components/Logo.vue';

const cameraFeedUrl = '/camera-feed'
</script>
