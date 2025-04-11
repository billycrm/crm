<template>
  <v-container>
    <v-row
      class="fill-height"
      align="center"
      justify="center"
    >
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5 text-center custom-card">
          <v-card-title>
            <h2 class="display-2 mb-4">Welcome to Gym Management, {{ user?.name }}! </h2>
          </v-card-title>
          <v-card-text>
            <v-row justify="center" class="mb-4">
              <div v-if="isAuthenticated">
                <v-col cols="12">
                  <v-btn
                    :to="{ name: 'Membership' }"
                    color="primary"
                    large
                    block
                    class="mb-3 custom-btn"
                  >
                    Go to Memberships
                  </v-btn>
                </v-col>
              </div>
              <div v-else>
                <v-col>
                  <v-btn
                    :to="{ name: 'Login' }"
                    color="primary"
                    large
                    block
                    class="mb-3 custom-btn"
                  >
                    Login
                  </v-btn>
                </v-col>
                <v-col>
                  <v-btn
                    :to="{ name: 'Register' }"
                    color="secondary"
                    large
                    block
                    class="custom-btn"
                  >
                    Register
                  </v-btn>
                </v-col>
              </div>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {usePiniaStore} from '../store/index.js';


export default {
  name: 'Home',
  setup() {
    const storePinia = usePiniaStore();

    return { storePinia };
  },
  data() {
  },
  computed: {
    user() {
      let user = this.storePinia.GUser
      if (!user) {
        this.storePinia.getUser();
      }
      return user;
    },
    isAuthenticated() {
      return this.storePinia.GIsAuthenticated
    }
  }
};
</script>

<style>
html, body, #app, .v-application {
  height: 100%;
  margin: 0;
}

.fill-height {
  height: 100%;
}

.mb-3 {
  margin-bottom: 1rem;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.custom-card {
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.custom-btn {
  font-weight: bold;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.custom-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.custom-btn:active {
  transform: translateY(1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}
</style>
