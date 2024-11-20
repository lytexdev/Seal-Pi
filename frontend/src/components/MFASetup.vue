<template>
    <div class="mfa-setup">
        <h3>MFA Setup</h3>

        <div class="totp-setup">
            <div v-if="totpEnabled">
                <button @click="deleteTOTP" class="button button-danger">Delete TOTP</button>
            </div>
            <div v-else>
                <div v-if="!verified">
                    <div v-if="!qrCodeUrl">
                        <button @click="setupTOTP" class="button">Setup TOTP</button>
                    </div>

                    <div v-if="qrCodeUrl">
                        <p>Scan this QR code with your authenticator app:</p>
                        <img :src="qrCodeUrl" class="totp-qrcode" alt="TOTP QRCode" />
                        <p>If you can't scan the QR code, use this secret key:</p>
                        <code>{{ secret }}</code>
                        <br>
                        <div class="form-group">
                            <label for="totp_code" class="label">Enter the code from your authenticator app:</label>
                            <input v-model="totpCode" type="text" id="totp_code" class="input" placeholder="Enter your TOTP code" />
                        </div>
                        <button @click="verifyTOTP" class="button">Verify TOTP</button>
                    </div>
                </div>

                <div v-if="verified">
                    <p>Setup complete! Here are your backup codes. Save them in a secure place:</p>
                    <ul class="backup-codes">
                        <li v-for="code in backupCodes" :key="code">{{ code }}</li>
                    </ul>
                    <button class="button" @click="finishSetup">Finish Setup</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import QRCode from 'qrcode'

const qrCodeUrl = ref(null)
const secret = ref(null)
const totpCode = ref('')
const backupCodes = ref([])
const verified = ref(false)
const totpEnabled = ref(false)

const fetchMFAStatus = async () => {
    try {
        const response = await axios.get('/api/mfa/status')
        totpEnabled.value = response.data.totp_enabled
    } catch (error) {
        console.error("Failed to fetch MFA status:", error)
    }
}

const setupTOTP = async () => {
    try {
        const response = await axios.post('/api/mfa/setup-totp')
        secret.value = response.data.secret
        qrCodeUrl.value = await QRCode.toDataURL(response.data.otp_url)
    } catch (error) {
        alert(error.response?.data?.message || "Failed to setup TOTP")
    }
}

const verifyTOTP = async () => {
    try {
        if (!totpCode.value) {
            alert("Please enter the TOTP code.")
            return
        }

        const response = await axios.post('/api/mfa/verify-totp', {
            totp_code: totpCode.value
        })
        backupCodes.value = response.data.backup_codes
        verified.value = true
    } catch (error) {
        alert(error.response?.data?.message || "Failed to verify TOTP")
    }
}

const finishSetup = async () => {
    alert("TOTP setup completed successfully!")
    await fetchMFAStatus()
    
    qrCodeUrl.value = null
    secret.value = null
    totpCode.value = ''
    verified.value = false
}

const deleteTOTP = async () => {
    if (!confirm("Are you sure you want to delete TOTP?")) return
    try {
        await axios.post('/api/mfa/delete-totp')
        alert("TOTP deleted successfully!")
        await fetchMFAStatus()
    } catch (error) {
        alert(error.response?.data?.message || "Failed to delete TOTP")
    }
}

fetchMFAStatus()
</script>
