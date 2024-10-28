<template>
    <section id="administration">
        <Logo title="Administration" />
        <Accordion title="User-Management" :defaultOpen="false">
            <ul>
                <li v-for="user in users" :key="user.id" class="user-item">
                    <b>{{ user.username }} <span v-if="user.is_admin" class="admin-badge">(Admin)</span></b>
                    <span>{{ user.email }}</span>
                    <div class="user-actions">
                        <button class="button button-secondary" @click="selectUser(user)">Edit</button>
                        <button class="button button-disabled" @click="deleteUser(user.id)">Delete</button>
                    </div>
                </li>
            </ul>

            <div class="add-user-form">
                <h3 v-if="!editMode">Add New User</h3>
                <h3 v-else>Edit User</h3>
                <div class="form-group">
                    <label class="label" for="username">Username</label>
                    <input v-model="userForm.username" type="text" id="username" class="input"
                        placeholder="Enter username" />
                </div>
                <div class="form-group">
                    <label class="label" for="email">Email</label>
                    <input v-model="userForm.email" type="email" id="email" class="input" placeholder="Enter email" />
                </div>
                <div class="form-group">
                    <label class="label" for="password">Password</label>
                    <input v-model="userForm.password" type="password" id="password" class="input"
                        placeholder="Enter password" />
                </div>
                <div class="form-group-checkbox">
                    <div class="form-group">
                        <label class="label" for="is_admin">Admin</label>
                        <input v-model="userForm.is_admin" type="checkbox" id="is_admin" />
                    </div>
                    <i>Only admin users can visit the administration page</i>
                </div>

                <div class="form-actions">
                    <button class="button" @click="editMode ? updateUser() : addUser()">
                        {{ editMode ? "Update User" : "Add User" }}
                    </button>
                    <button class="button button-secondary" v-if="editMode" @click="cancelEdit">Cancel</button>
                </div>
            </div>
        </Accordion>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Logo from '../components/Logo.vue'
import Accordion from '../components/Accordion.vue'

const users = ref([])
const editMode = ref(false)
const userForm = ref({
    id: null,
    username: '',
    email: '',
    password: '',
    is_admin: false
})

const fetchUsers = async () => {
    try {
        const response = await axios.get('/api/users')
        users.value = response.data
    } catch (error) {
        console.error("Error fetching users:", error)
    }
}

const addUser = async () => {
    try {
        await axios.post('/api/users', userForm.value)
        fetchUsers()
        resetForm()
    } catch (error) {
        console.error("Error adding user:", error)
    }
}

const selectUser = (user) => {
    userForm.value = { ...user, password: '' }
    editMode.value = true
}

const updateUser = async () => {
    try {
        if (!confirm("Are you sure you want to update this user?")) {
            return
        }

        await axios.put(`/api/users/${userForm.value.id}`, userForm.value)
        fetchUsers()
        resetForm()
    } catch (error) {
        console.error("Error updating user:", error)
    }
}

const deleteUser = async (id) => {
    try {
        if (!confirm("Are you sure you want to delete this user?")) {
            return
        }
        await axios.delete(`/api/users/${id}`)
        fetchUsers()
    } catch (error) {
        console.error("Error deleting user:", error)
    }
}

const resetForm = () => {
    userForm.value = { id: null, username: '', email: '', password: '', is_admin: false }
    editMode.value = false
}

const cancelEdit = () => {
    resetForm()
}

onMounted(() => {
    fetchUsers()
})
</script>