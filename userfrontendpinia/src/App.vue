<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>Billy CRM</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">Home</v-btn>
      <v-btn v-if="!isAuthenticated" to="/login">Login</v-btn>
      <v-btn v-if="!isAuthenticated" to="/register">Register</v-btn>
      <v-btn v-if="isAuthenticated" to="/membership">Membership</v-btn>
      <v-btn v-if="isAuthenticated" @click="logout">Logout</v-btn>
      <span v-if="user">({{ user.name }})</span>
    </v-app-bar>
    <v-main>
      <v-container class="d-flex justify-center align-center" style="height: 100vh;">
        <v-row align="center" justify="center">
          <v-col cols="12" md="8">
            <router-view />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import {usePiniaStore} from "@/store/index.js";

export default {
  setup() {
    const storePinia = usePiniaStore();

    return { storePinia };
  },
  data() {
  },
  computed: {
    isAuthenticated() {
      return this.storePinia.GIsAuthenticated;
    },
    user() {
      return this.storePinia.GUser;
    },
  },
  methods: {
    logout() {
      this.storePinia.logout();
    },
  },
};
</script>

<style>
html, body, #app, .v-application {
  height: 100%;
  margin: 0;
}
</style>
