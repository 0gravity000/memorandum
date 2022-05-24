<template>
  <div class="tags-index">
    <a href="#" @click="authLogout">ログアウト</a>
    <h2>タグ一覧</h2>
    <router-link to="/tags/create">タグ登録</router-link>&nbsp;
    <router-link to="/bookmarks">ブックマーク一覧</router-link>&nbsp;
    <hr>
    <span v-for="tag in tags" :key="tag">
      <span class="tag-name">
        {{tag.name}}&nbsp;
      </span>
      <span class="tag-remarks">
        {{tag.remarks}}&nbsp;
      </span>
      <router-link :to="{name: 'tags-update', params: {id: tag.id}}">編集</router-link>&nbsp;
      <a href="" @click="deleteTags(tag.id)">削除</a>&nbsp;
      /&nbsp;
    </span>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
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
    confirmDelete() {
      return confirm("タグを削除します")
    },    
    authLogout: function(){
      //let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/auth/logout')
      .then(function (res) {
        console.log(res.data)
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