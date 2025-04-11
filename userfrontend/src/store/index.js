// store/index.js
import Vuex from 'vuex';
import router from "@/router/index.js";
import axios from 'axios';

export default new Vuex.Store({
  state: {
    isAuthenticated: !!localStorage.getItem('token'),
    token: localStorage.getItem('token'),
    user: null,
    memberships: [],
    lastFetched: null,
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    token: (state) => state.token,
    memberships: (state) => state.memberships,
    user: (state) => {
      if (state.user) {
        return state.user;
      } else {
        return null;
      }
    }
  },
  mutations: {
    SET_AUTH(state, value) {
      state.isAuthenticated = value;
    },
    SET_ACCESS_TOKEN(state, value) {
      state.token = value;
    },
    SET_MEMBERSHIPS(state, memberships) {
      state.memberships = memberships;
    },
    SET_USER(state, user) {
      state.user = user;
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
      commit('SET_ACCESS_TOKEN', null);
      commit('SET_USER', null);
      router.push('/');
    },
    async getUser({commit, state}) {
      if (!state.token) {
        console.error('No token found, user not authenticated');
        return;
      }
      if (state.user) {
        console.log('User data already in state:', state.user);
        return;
      }
      try {
        const response = await axios.get('http://localhost:5000/api/v1/users/1', {
          headers: {
            Authorization: `Bearer ${state.token}`,
          }
        });
        commit('SET_USER', response.data);
        console.log('User data fetched:', response.data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async getMemberships({commit, state}) {
      if (state.lastFetched && (Date.now() - state.lastFetched < 60000)) {
        console.log('Using cached memberships');
        return;
      }
      try {
        const response = await axios.get('http://localhost:5000/api/v1/memberships', {
          headers: {
            Authorization: `Bearer ${state.token}`,
          }
        });
        commit('SET_MEMBERSHIPS', response.data);
        console.log(state.memberships)
      } catch (error) {
        console.log('No memberships found.', error);
      }
    }
  },
});
