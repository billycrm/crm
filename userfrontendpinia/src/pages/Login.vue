<template>
  <v-container>
    <v-row
      class="fill-height"
      align="center"
      justify="center"
    >
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-5">
          <v-card-title class="headline">Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="username"
                label="Username"
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
              <v-spacer class="mb-4"></v-spacer>
              <v-btn type="submit" color="primary" block>Login</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from 'axios';
import {piniaStore} from '../store/index.js';

const store = piniaStore();
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      // validate
      try {
        const response = await axios.post('http://localhost:5000/api/v1/login', {
          username: this.username,
          password: this.password
        });
        // call login action from Vuex store
        store.dispatch('login', response.data.access_token);
        this.$router.push({ name: 'Membership' });
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
