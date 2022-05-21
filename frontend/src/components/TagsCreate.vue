<template>
  <div class="tags-create">
    <h2>タグ登録</h2>
    <router-link to="/tags">戻る</router-link>
    <form class=" me-5">
      <div class="mb-3">
        <label class="form-label">タグ名</label>
        <input v-model="this.name" class="form-control" placeholder="タグ名を入力してください">
      </div>
      <div class="mb-3">
        <label class="form-label">備考</label>
        <input v-model="this.remarks" class="form-control" placeholder="備考を入力してください">
      </div>
      <button type="button" @click="createTag" class="btn btn-primary">登録</button>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  data() {
    return {
      name: "",
      remarks: "",
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
    createTag: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/tags', {
        name: self.name,
        remarks: self.remarks,
      })
      .then(function (res) {
        console.log(res.data)
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
