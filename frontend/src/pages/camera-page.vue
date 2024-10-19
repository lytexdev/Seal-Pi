<template>
    <section id="liveCamera">
        <Logo title="LIVE CAMERA" />

        <div class="camera-info flex">
            <span>
                <strong>Slot:</strong> {{ cameraInfo.camera_slot }}
            </span>
            <span>
                <strong>FPS:</strong> {{ cameraInfo.camera_framerate }}
            </span>
            <span>
                <strong>Current Time:</strong> {{ cameraInfo.current_time }}
            </span>
        </div>

        <div class="camera-feed">
            <img :src="cameraFeedUrl" alt="Live Camera">
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Logo from '../components/Logo.vue'

const cameraFeedUrl = '/api/camera-feed'

const cameraInfo = ref({
    camera_slot: '',
    camera_framerate: '',
    current_time: ''
})

const fetchCameraInfo = async () => {
    try {
        const response = await axios.get('/api/camera-info')
        cameraInfo.value = response.data
    } catch (error) {
        console.error('Error fetching camera info:', error)
    }
}

onMounted(() => {
    fetchCameraInfo()
    setInterval(fetchCameraInfo, 1000)
})
</script>
