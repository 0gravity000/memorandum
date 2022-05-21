<template>
  <div class="tags-index">
    <h2>タグ一覧</h2>
    <router-link to="/tags/create">タグ登録</router-link>&nbsp;
    <router-link to="/bookmarks">ブックマーク一覧</router-link>&nbsp;
    <div v-for="tag in tags" :key="tag">
      <div class="card me-3">
        <div class="card-body">
          <h5 class="card-title">{{tag.name}}</h5>
          <h6 class="card-subtitle mb-2 text-muted fw-light">{{tag.remarks}}</h6>
          <router-link :to="{name: 'tags-update', params: {id: tag.id}}">タグ編集</router-link>&nbsp;
          <a href="" @click="deleteTags(tag.id)">タグ削除</a>
        </div>
      </div>
    </div>
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