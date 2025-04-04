// store/index.js
import Vuex from 'vuex';
import router from "@/router/index.js";

export default new Vuex.Store({
  state: {
    isAuthenticated: !!localStorage.getItem('token'),
  },
  mutations: {
    SET_AUTH(state, value) {
      state.isAuthenticated = value;
    },
  },
  actions: {
    login({ commit }, token) {
      localStorage.setItem('token', token);
      commit('SET_AUTH', true);
    },
    logout({ commit }) {
      localStorage.removeItem('token');
      commit('SET_AUTH', false);
      router.push('/');
    },
  },
});
