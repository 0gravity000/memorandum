<template>
  <div class="bookmarks-create">
    <h2>ブックマーク登録</h2>
    <router-link to="/bookmarks">戻る</router-link>
    <form class=" me-5">
      <div class="mb-3">
        <label class="form-label">タイトル</label>
        <input v-model="this.title" class="form-control" placeholder="タイトルを入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">URL</label>
        <input v-model="this.url" class="form-control" placeholder="URLを入力してください">
      </div>
      <div class="mb-3 col-6">
        <label class="form-label">重要度</label>
        <div class="row">
          <div class="col">
            <label class="form-label">低</label>
          </div>
          <div class="col range-label-end">
            <label class="form-label">高</label>
          </div>
        </div>
        <div class="row">
          <input v-model="this.importance" type="range" class="form-range" min="1" max="5">
        </div>
      </div>
      <div class="mb-3">
        <label class="form-label">備考</label>
        <input v-model="this.remarks" class="form-control" placeholder="備考を入力してください">
      </div>

      <label class="form-label">タグ</label>
      <div class="col mb-3">
        <span v-for="tag in tags" :key="tag">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" :value="tag.id" v-model="checkedTags">
            <label class="form-check-label">{{tag.name}}</label>
          </div>         
        </span>
      </div>

      <button type="button" @click="createBookmark" class="btn btn-primary">登録</button>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  data() {
    return {
      title: "",
      url: "",
      remarks: "",
      importance: 3,
      tags: [],
      checkedTags: [],
    }
  },
  mounted() {
    this.indexTags()
  },
  computed: {
  },
  methods: {
    indexTags: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/tags')
      .then(function (res) {
        console.log(res.data)
        self.tags = res.data
      })
      .catch(function (err){
        console.log(err)
      })
    },
    createBookmark: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/bookmarks', {
        title: self.title,
        url: self.url,
        remarks: self.remarks,
        importance: self.importance,
        checkedTags: self.checkedTags,
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
.range-label-end {
  text-align: end;
}
</style>
