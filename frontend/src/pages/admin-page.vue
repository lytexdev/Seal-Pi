<template>
    <section id="administration">
        <Logo title="Administration" />

        <section class="user-section">
            <h2>Users</h2>
            <ul>
                <li class="user-item">
                    <b>lytex</b>
                    <div class="user-actions">
                        <button class="button button--secondary">Edit</button>
                        <button class="button button--disabled">Delete</button>
                    </div>
                </li>
            </ul>

            <div class="add-user-form">
                <h3>Add New User</h3>
                <div class="form-group">
                    <label class="label" for="username">Username</label>
                    <input  type="text" id="username" class="input" placeholder="Enter username" />
                </div>
                <div class="form-group">
                    <label class="label" for="email">Email</label>
                    <input type="email" id="email" class="input" placeholder="Enter email" />
                </div>
                <div class="form-group">
                    <label class="label" for="password">Password</label>
                    <input type="password" id="password" class="input" placeholder="Enter password" />
                </div>
                <div class="form-actions">
                    <button class="button">Add User</button>
                </div>
            </div>
        </section>
    </section>
</template>

<script setup>
import Logo from '../components/Logo.vue'
</script>
