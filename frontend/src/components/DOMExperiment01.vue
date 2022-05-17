<template>
  <div class="dom-experiment-01">
    <h2>指定ページのa要素と全テキストを出力する</h2>
    <!-- 
    <form action="/api/stroke/ahref" method="post">
    -->
    <form>
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">URL</label>
        <input v-model="this.targetUrl" class="form-control" placeholder="URLを入力してください">
      </div>
      <button type="button" @click="crawlTargetUrl" class="btn btn-primary">送信</button>
      <!--
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">セレクター</label>
        <input v-model="this.targetSelector" class="form-control" placeholder="セレクターを入力してください">
      </div>
      <button type="submit" class="btn btn-primary">送信</button>
      -->
    </form>

    <hr>
    <div>
      <a href="#dom-experiment-01-result-a-tag">a要素の出力結果へ</a>
    </div>
    <div>
      <a href="#dom-experiment-01-result-all-text">全テキストの出力結果へ</a>
    </div>

    <hr>
    <h3 id="dom-experiment-01-result-a-tag">a要素</h3>
    <div v-for="element in elements" :key="element" class="mt-3">
      {{element.txt}}<br>
      <a :href="targetProtocol + '//' + targetDomein + '/' + element.href" target="_blank" rel="noopener noreferrer">
        {{targetProtocol}}//{{targetDomein}}/{{element.href}}
      </a>
    </div>

    <hr>
    <h3 id="dom-experiment-01-result-all-text">全テキスト</h3>
    <div v-for="text in texts" :key="text">
      {{text}}<br>
    </div>
    <!-- 
    <div>{{targetAllText}}</div>
    <div v-for="element in elements" :key="element">
      <a :href="element.href" target="_blank" rel="noopener noreferrer">{{element.innerHTML}}</a>
    </div>
    <div>{{elements}}</div>
     -->
  </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios').default

export default {
  data() {
    return {
      targetUrl: "https://developer.mozilla.org/ja/docs/Web/API",
      targetDomein: "",
      targetProtocol: "",
      targetAllText: "",
      //targetSelector: "a",
      elements: [],
      texts: [],
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
    crawlTargetUrl: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      let uri = new URL(this.targetUrl)
      this.targetDomein = uri.hostname
      this.targetProtocol = uri.protocol
      axios.post('/api/stroke/ahref', { //バックエンドでbodyとして取得できる
        targetUrl: self.targetUrl,
        targetSelector: self.targetSelector,
      })
      .then(function (res) {
        console.log(res.data)
        self.elements = res.data[0]
        self.splitEachText(res.data[1])
        //self.targetAllText = res.data[1]
      })
      .catch(function (err){
        console.log(err)
        self.elements = err.data
      })
    },
    splitEachText:  function(alltexts) {
      this.texts = alltexts.split("｜")
    },
  },
}
</script>