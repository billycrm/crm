// store/index.js
import Vuex from 'vuex';
import router from "@/router/index.js";
import axios from 'axios';

export default new Vuex.Store({
  state: {
    isAuthenticated: !!localStorage.getItem('token'),
    token: null,
    memberships: null,
    lastFetched: null,
  },
  mutations: {
    SET_AUTH(state, value) {
      state.isAuthenticated = value;
    },
    SET_ACCESS_TOKEN(state, user) {
      state.token = user;
    },
  },
  actions: {
    login({ commit }, token) {
      localStorage.setItem('token', token);
      commit('SET_AUTH', true);
      commit('SET_ACCESS_TOKEN', token);
    },
    logout({ commit }) {
      localStorage.removeItem('token');
      commit('SET_AUTH', false);
      router.push('/');
    },
    getMemberships({ commit }) {
      if (this.memberships && this.lastFetched && (Date.now() - this.lastFetched < 60000)) {
        console.log('Using cached memberships');
        return;
      }
      try {
        const response = axios.get('http://localhost:5000/api/v1/memberships', {
          headers: {
            Authorization: `Bearer ${this.state.user}`,
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
