import { createStore } from 'vuex'

export default createStore({
  state: {
    authUserid: "",
    authEmail: "",
    authNickname: "",
  },
  getters: {
  },
  mutations: {
    setAuthUser(state, user) {
      state.authUserid = user.id
      state.authEmail = user.email
      state.authNickname = user.nickname
    },
    clearAuthUser(state) {
      state.authUserid = ""
      state.authEmail = ""
      state.authNickname = ""
    }
  },
  actions: {
  },
  modules: {
  }
})
