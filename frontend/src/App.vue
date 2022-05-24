<template>
  <div class="container-fluid">
    <NavbarMain />
    <div class="row">
      <div class="col-3">
        <SidebarHome />
      </div>
      <div class="col-9">
        <router-view
          :authUser="authUser"
          @update-auth-notification="updateAuthInfo"
        />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavbarMain from '@/components/NavbarMain.vue'
import SidebarHome from '@/components/SidebarHome.vue'

const axios = require('axios').default

export default {
  components: {
    NavbarMain,
    SidebarHome,
  },
  data () {
    return {
      authUser: {
        id: "",
        email: "ゲスト",
        password: "",
        nickname: "",
      }
    }
  },
  created() {
    //リロードされたとき認証ユーザーを再取得する
    this.checkAuthUser()
  },
  methods: {
    checkAuthUser() {
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/auth/check')
      .then(function (res) {
      console.log("app.vue：checkAuthUser")
        console.log(res.data)
        self.authUser = res.data
      })
      .catch(function (err){
        console.log(err)
      })
    },
    updateAuthInfo(data) {
      console.log("app.vue：updateAuthInfo")
      console.log(data)
      this.authUser = data
    },
  }
}
</script>

<style>
</style>