<template>
  <div class="tags-update">
    <h2>タグ編集</h2>
    <router-link to="/tags">戻る</router-link>
    <form>
      <label class="form-label">{{ id }}</label>
      <div class="mb-3">
        <label class="form-label">タグ名</label>
        <input v-model="this.tags.name" class="form-control" placeholder="タグ名を入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">備考</label>
        <input v-model="this.tags.remarks" class="form-control" placeholder="備考を入力してください">
      </div>
      <button type="button" @click="updateTag" class="btn btn-primary">更新</button>
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
      tags: [],
    }
  },
  mounted() {
    this.id = this.$route.params.id
    this.showTag()
  },
  computed: {
  },
  methods: {
    showTag: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/tags/show', {
        params: {
          id: this.id,
        }
      })
      .then(function (res) {
        console.log(res.data)
        self.tags = res.data
      })
      .catch(function (err){
        console.log(err)
      })
    },
    updateTag: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.put('/api/tags/update/' + this.id, {
        //id: this.id,
        name: this.tags.name,
        remarks: this.tags.remarks,
      })
      .then(function (res) {
        console.log(res.data)
        self.tags = res.data
        self.$router.push({name: "tags-index"})
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
