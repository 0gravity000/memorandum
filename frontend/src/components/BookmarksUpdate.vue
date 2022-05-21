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
          <input v-model="this.bookmarks.importance" type="range" class="form-range" min="1" max="5">
        </div>
      </div>
      <div class="mb-3">
        <label class="form-label">備考</label>
        <input v-model="this.bookmarks.remarks" class="form-control" placeholder="備考を入力してください">
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
      tags: [],
      bookmark_tags: [],
      checkedTags: [],
    }
  },
  mounted() {
    this.id = this.$route.params.id
    this.showBookmark()
  },
  computed: {
  },
  methods: {
    isCheckedTag: function() {
      console.log("isCheckedTag")
      console.log(this.bookmark_tags)
      if(this.bookmark_tags == "") {
        return
      }
      //console.log(this.bookmark_tags.length)
      let array = []
      for(let i = 0; i < this.bookmark_tags.length; i++) {
        console.log(this.bookmark_tags[i])
        array.push(this.bookmark_tags[i].tag_id)
      }
      this.checkedTags = Array.from(new Set(array))
      return
    },
    showBookmark: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/bookmarks/show', {
        params: {
          id: this.id,
        }
      })
      .then(function (res) {
        console.log(res.data)
        self.bookmarks = res.data[0]
        self.tags = res.data[1]
        self.bookmark_tags = res.data[2]
        self.isCheckedTag()
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
        importance: this.bookmarks.importance,
        checkedTags: this.checkedTags,
      })
      .then(function (res) {
        console.log(res.data)
        self.bookmarks = res.data[0]
        self.tags = res.data[1]
        self.bookmark_tags = res.data[2]
        self.isCheckedTag()
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
