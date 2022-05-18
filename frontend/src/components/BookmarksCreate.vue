<template>
  <div class="bookmarks-create">
    <h2>ブックマーク登録</h2>
    <router-link to="/bookmarks">戻る</router-link>
    <form>
      <div class="mb-3">
        <label class="form-label">タイトル</label>
        <input v-model="this.title" class="form-control" placeholder="タイトルを入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">URL</label>
        <input v-model="this.url" class="form-control" placeholder="URLを入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">備考</label>
        <input v-model="this.remarks" class="form-control" placeholder="備考を入力してください">
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
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
    createBookmark: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/bookmarks', {
        title: self.title,
        url: self.url,
        remarks: self.remarks,
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