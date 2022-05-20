<template>
  <div class="bookmarks-index">
    <h2>ブックマーク一覧</h2>
    <router-link to="/bookmarks/create">ブックマーク登録</router-link>&nbsp;
    <div class="row">
      <div class="col">
        <span>ソート</span>&nbsp;
        登録日&nbsp;
        <span>
          <button type="button" @click="showBookmarks(1, 1)">▲</button>&nbsp;
          <button type="button" @click="showBookmarks(1, 2)">▼</button>&nbsp;
        </span>
        更新日&nbsp;
        <span>
          <button type="button" @click="showBookmarks(2, 1)">▲</button>&nbsp;
          <button type="button" @click="showBookmarks(2, 2)">▼</button>&nbsp;
        </span>
        url&nbsp;
        <span>
          <button type="button" @click="showBookmarks(3, 1)">▲</button>&nbsp;
          <button type="button" @click="showBookmarks(3, 2)">▼</button>&nbsp;
        </span>
        重要度&nbsp;
        <span>
          <button type="button" @click="showBookmarks(4, 1)">▲</button>&nbsp;
          <button type="button" @click="showBookmarks(4, 2)">▼</button>&nbsp;
        </span>
      </div>
    </div>
    <!-- {{bookmarks}}<br> -->
    <div v-for="bookmark in bookmarks" :key="bookmark">
      <div class="card me-3">
        <div class="card-body">
          <span v-for="i in bookmark.importance" :key="i">{{"★"}}</span>
          <!-- 
          <h6 class="card-subtitle mb-2 text-muted fw-light">{{bookmark.id}}</h6>
           -->
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
      bookmarks: [],
      sortItem: "",
      sortAsc: "",
    }
  },
  mounted() {
    this.showBookmarks(this.sortItem, this.sortAsc)
    console.log("mounted exec this.showBookmarks() ")
  },
  computed: {
  },
  methods: {
    confirmDelete() {
      return confirm("ブックマークを削除します")
    },    
    showBookmarks: function(sortItem, sortAsc){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/bookmarks', {
        params: {
          sortItem: sortItem,
          sortAsc: sortAsc,
        }
      })
      .then(function (res) {
        console.log(res.data)
        self.bookmarks = res.data[0]
        self.sortItem = res.data[1]
        self.sortAsc = res.data[2]
      })
      .catch(function (err){
        console.log(err)
        self.bookmarks = err.data[0]
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