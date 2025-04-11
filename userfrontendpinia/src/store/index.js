// store/index.js
import {defineStore} from 'pinia'
import router from "@/router/index.js";
import axios from 'axios';

export const usePiniaStore = defineStore('piniaStore', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('token'),
    token: localStorage.getItem('token'),
    user: null,
    memberships: [],
    lastFetched: null,
  }),
  getters: {
    GIsAuthenticated: (state) => state.isAuthenticated,
    GToken: (state) => state.token,
    GMemberships: (state) => state.memberships,
    GUser: (state) => {
      if (state.user) {
        return state.user;
      } else {
        return null;
      }
    },
    GLastFetched: (state) => {
      return state.lastFetched;
    },
  },
  actions: {
    async login(token) {
      localStorage.setItem('token', token);
      this.token = token;
      this.isAuthenticated = true;
      await this.getUser();
    },
    logout() {
      localStorage.removeItem('token');
      this.token = null;
      this.isAuthenticated = false;
      this.user = null;
      router.push('/');
    },
    async getUser() {
      if (!this.token) {
        console.error('No token found, user not authenticated');
        return;
      }
      if (this.user) {
        console.log('User data already in state:', this.user);
        return;
      }
      try {
        const response = await axios.get('http://localhost:5000/api/v1/users/1', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          }
        });

        this.user = response.data;
        console.log('User data fetched:', response.data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async getMemberships() {
      if (this.lastFetched && (Date.now() - this.lastFetched < 60000)) {
        console.log('Using cached memberships');
        return;
      }
      try {
        const response = await axios.get('http://localhost:5000/api/v1/memberships', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          }
        });
        this.memberships = response.data;
        console.log(this.memberships)
      } catch (error) {
        console.log('No memberships found.', error);
      }
    }
  },
});
