<template>
  <div class="bookmarks-update">
    <h2>ブックマーク編集</h2>
    <router-link to="/bookmarks">戻る</router-link>
    <form>
      <label class="form-label">{{ id }}</label>
      <div class="mb-3">
        <label class="form-label">タイトル</label>
        <input v-model="this.bookmarks.title" class="form-control" placeholder="タイトルを入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">URL</label>
        <input v-model="this.bookmarks.url" class="form-control" placeholder="URLを入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">備考</label>
        <input v-model="this.bookmarks.remarks" class="form-control" placeholder="備考を入力してください">
      </div>
      <button type="button" @click="updateBookmark" class="btn btn-primary">更新</button>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  data() {
    return {
      id: "",
      bookmarks: [],
    }
  },
  mounted() {
    this.id = this.$route.params.id
    this.showBookmark()
  },
  computed: {
  },
  methods: {
    showBookmark: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/bookmarks/show', {
        params: {
          id: this.id,
        }
      })
      .then(function (res) {
        console.log(res.data)
        self.bookmarks = res.data
      })
      .catch(function (err){
        console.log(err)
      })
    },
    updateBookmark: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.put('/api/bookmarks/update/' + this.id, {
        //id: this.id,
        title: this.bookmarks.title,
        url: this.bookmarks.url,
        remarks: this.bookmarks.remarks,
      })
      .then(function (res) {
        console.log(res.data)
        self.bookmarks = res.data
      })
      .catch(function (err){
        console.log(err)
      })
    },
  },
}
</script>