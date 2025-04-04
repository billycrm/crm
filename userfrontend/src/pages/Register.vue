<template>
  <v-container>
    <v-row
      class="fill-height"
      align="center"
      justify="center"
    >
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5">
          <v-card-title class="text-center">
            <h2 class="display-1">Register</h2>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="register">
              <v-text-field
                v-model="username"
                label="Username"
                required
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="name"
                label="Name"
                required
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="email"
                label="Email"
                required
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
                class="mb-4"
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                large
              >
                Register
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      name: '',
      email: '',
      password: ''
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('http://localhost:5000/api/v1/register', {
          username: this.username,
          name: this.name,
          email: this.email,
          password: this.password
        });
        this.$router.push({ name: 'Login' });
      } catch (error) {
        alert('Registration failed');
      }
    }
  }
};
</script>
