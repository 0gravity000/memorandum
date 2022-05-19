<template>
  <div class="bookmarks-index">
    <h2>ブックマーク一覧</h2>
    <router-link to="/bookmarks/create">ブックマーク登録</router-link>
    <!-- {{bookmarks}}<br> -->
    <div v-for="bookmark in bookmarks" :key="bookmark">
      <div class="card me-3">
        <div class="card-body">
          <h6 class="card-subtitle mb-2 text-muted fw-light">{{bookmark.id}}</h6>
          <h5 class="card-title" data-bs-toggle="tooltip" :title="bookmark.remarks">{{bookmark.title}}</h5>
          <a :href="bookmark.url" target="_blank" rel="noopener noreferrer">
            <p class="card-text">{{bookmark.url}}</p>
          </a>
        <router-link :to="{name: 'bookmarks-update', params: {id: bookmark.id}}">ブックマーク編集</router-link>&nbsp;
        <a href="" @click="deleteBookmarks(bookmark.id)">ブックマーク削除</a>
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
      bookmarks: []
    }
  },
  mounted() {
    this.showBookmarks()
  },
  computed: {
  },
  methods: {
    confirmDelete() {
      return confirm("ブックマークを削除します")
    },    
    showBookmarks: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/bookmarks')
      .then(function (res) {
        console.log(res.data)
        self.bookmarks = res.data
      })
      .catch(function (err){
        console.log(err)
        self.bookmarks = err.data
      })
    },
    deleteBookmarks: function(id){
      if (this.confirmDelete()) {
        let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
        axios.delete('/api/bookmarks/delete/' + id)
        .then(function (res) {
          console.log(res.data)
          self.bookmarks = res.data
        })
        .catch(function (err){
          console.log(err)
          self.bookmarks = err.data
        })
      }
    },
  },
}
</script>