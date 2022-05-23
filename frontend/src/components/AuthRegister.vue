<template>
  <div class="auth-register">
    <h2>ユーザー登録</h2>
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
      <div class="mb-3">
        <label class="form-label">ニックネーム</label>
        <input v-model="this.nickname" class="form-control" placeholder="備考を入力してください">
      </div>

      <button type="button" @click="authRegister" class="btn btn-primary">登録</button>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  data() {
    return {
      email: "",
      password: "",
      nickname: "",
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
    authRegister: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/auth/register', {
        email: self.email,
        password: self.password,
        nickname: self.nickname,
      })
      .then(function (res) {
        console.log(res.data)
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
