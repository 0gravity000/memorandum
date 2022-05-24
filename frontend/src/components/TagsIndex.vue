<template>
  <div class="tags-index">
    <p>{{authEmailOrNickname()}}&nbsp;さん
      <a href="#" @click="authLogout">ログアウト</a>
    </p>
    <h2>タグ一覧</h2>
    <span v-show="isAdminUser()">
      <router-link to="/tags/create">タグ登録</router-link>&nbsp;
    </span>
    <router-link to="/bookmarks">ブックマーク一覧</router-link>&nbsp;
    <hr>
    <span v-for="tag in tags" :key="tag">
      <span class="tag-name">
        {{tag.name}}&nbsp;
      </span>
      <span class="tag-remarks">
        {{tag.remarks}}&nbsp;
      </span>
      <span v-show="isAdminUser()">
        <router-link :to="{name: 'tags-update', params: {id: tag.id}}">編集</router-link>&nbsp;
        <a href="" @click="deleteTags(tag.id)">削除</a>&nbsp;
      </span>
      /&nbsp;
    </span>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  props: {
    authUser: {
      type : Object,
    }
  },
  data() {
    return {
      tags: [],
    }
  },
  mounted() {
    this.showTags()
    console.log("mounted exec this.showTags() ")
  },
  computed: {
  },
  methods: {
    authEmailOrNickname(){
      if (this.authUser.nickname == "") {
        return this.authUser.email
      }
      return this.authUser.nickname
    },
    isAdminUser(){
      if (this.authUser.email == "0gravity000@gmail.com") {
        return true
      }
      return false
    },
    confirmDelete() {
      return confirm("タグを削除します")
    },    
    authLogout: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/auth/logout')
      .then(function (res) {
        console.log(res.data)
        let resdate = {id: "", email: "ゲスト", password: "", nickname: ""}
        self.$emit('update-auth-notification', resdate)
        //self.$store.commit('clearAuthUser')  //vuexのstateで管理
      })
      .catch(function (err){
        console.log(err)
      })
    },
    showTags: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/tags')
      .then(function (res) {
        console.log(res.data)
        self.tags = res.data
      })
      .catch(function (err){
        console.log(err)
        self.tags = err.data
      })
    },
    deleteTags: function(id){
      if (this.confirmDelete()) {
        let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
        axios.delete('/api/tags/delete/' + id)
        .then(function (res) {
          console.log(res.data)
          self.tags = res.data
        })
        .catch(function (err){
          console.log(err)
          self.tags = err.data
        })
      }
    },
  },
}
</script>

<style scoped>
.tag-name {
  font-size: 1.2rem;
  font-weight: bold;
}
.tag-remarks {
  font-size: 0.9rem;
  font-weight: lighter;
}

</style>