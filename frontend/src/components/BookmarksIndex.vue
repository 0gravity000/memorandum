<template>
  <div class="bookmarks-Index">
    <h2>ブックマーク一覧</h2>
    <router-link to="/bookmarks/create">ブックマーク登録</router-link>
    <!-- {{bookmarks}}<br> -->
    <div v-for="bookmark in bookmarks" :key="bookmark">
      {{bookmark.id}}<br>
      {{bookmark.title}}<br>
      {{bookmark.url}}<br>
      {{bookmark.remarks}}<br>
      <span>
        <router-link :to="{name: 'bookmarks-update', params: {id: bookmark.id}}">ブックマーク編集</router-link>&nbsp;
        <button @click="deleteBookmarks(bookmark.id)">ブックマーク削除</button>
        <!-- 
        <a :href="deleteBookmarks(bookmark.id)">ブックマーク削除</a>
         -->
      </span>
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
    },
  },
}
</script>