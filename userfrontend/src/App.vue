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
import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState(['isAuthenticated']),
  },
  methods: {
    ...mapActions(['login', 'logout']),
  },
};
</script>

<style>
html, body, #app, .v-application {
  height: 100%;
  margin: 0;
}
</style>
