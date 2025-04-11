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
                :rules="[
                  (v) => !!v || 'Username is required',
                  ]"
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
                type="email"
                :rules="[
                  (v) => !!v || 'Email is required',
                  (v) => /.+@.+\..+/.test(v) || 'Email must be valid'
                ]"
                required
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
                class="mb-4"
                :rules="[
                  (v) => !!v || 'Password is required',
                  ]"
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
      // validate
      if (!this.username || !this.name || !this.email || !this.password) {
        alert('Please fill in all fields.');
        return;
      }
      try {
        await axios.post('http://localhost:5000/api/v1/register', {
          username: this.username,
          name: this.name,
          email: this.email,
          password: this.password
        });
        this.$router.push({ name: 'Login' });
      } catch (error) {

        if (error.response && error.response.status === 400) {
          console.error('Login failed:', error.response.data.message);
          alert('Login failed: ' + error.response.data.message);
        } else {
          console.error('An unexpected error occurred:', error);
          alert('An unexpected error occurred. Please try again later.');
        }
      }
    }
  }
};
</script>
