<template>
  <div class="auth-login">
    <h2>ログイン</h2>
    <router-link to="/">戻る</router-link>
    <form class=" me-5">
      <div class="mb-3">
        <label class="form-label">email</label>
        <input v-model="this.email" type="email" class="form-control" placeholder="emailを入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">パスワード</label>
        <input v-model="this.password" type="password" class="form-control" placeholder="パスワードを入力してください">
      </div>

      <button type="button" @click="authLogin" class="btn btn-primary">送信</button>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  data() {
    return {
      authUser: {},
      email: "",
      password: "",
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
    authLogin: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/auth/login', {
        email: self.email,
        password: self.password,
        nickname: self.nickname,
      })
      .then(function (res) {
        console.log(res.data)
        self.authUser = res.data
        self.$emit('update-auth-notification', res.data)
        //self.$store.commit('setAuthUser', self.authUser)  //vuexのstateで管理
        self.$router.push({name: "bookmarks-index"})
      })
      .catch(function (err){
        console.log(err)
      })
    },
  },
}
</script>

<style scoped>

</style>
