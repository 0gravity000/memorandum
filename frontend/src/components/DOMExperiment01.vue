<template>
  <div class="dom-experiment-01">
    <p>{{authEmailOrNickname()}}&nbsp;さん
      <a href="#" @click="authLogout">ログアウト</a>
    </p>
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
      <div v-if="hasHrefProtocol(element.href)">
        <a :href="element.href" target="_blank" rel="noopener noreferrer">
          {{element.href}}
        </a>
      </div>
      <div v-else>
        <a :href="removeTargetUrlHash() + element.href" target="_blank" rel="noopener noreferrer">
          {{removeTargetUrlHash()}}{{element.href}}
        </a>
        <!-- こっちでうまくいくサイトもあるので、両方表示することにする -->
        <br>
        <a :href="targetProtocol + '//' + targetDomein + element.href" target="_blank" rel="noopener noreferrer">
          {{targetProtocol}}//{{targetDomein}}{{element.href}}
        </a>
      </div>      
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
  props: {
    authUser: {
      type : Object,
    }
  },
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
    authEmailOrNickname(){
      if (this.authUser.nickname == "") {
        return this.authUser.email
      }
      return this.authUser.nickname
    },
    authLogout: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/auth/logout')
      .then(function (res) {
        console.log(res.data)
        let resdate = {id: "", email: "ゲスト", password: "", nickname: ""}
        self.$emit('update-auth-notification', resdate)
        //self.$store.commit('clearAuthUser')  //vuexのstateで管理
      })
      .catch(function (err){
        console.log(err)
      })
    },
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
    hasHrefProtocol(element_href){
      //サイトによって、a要素で取得したhrefにプロトコルとドメインが含まれていない場合があるのでチェックする
      let re = /^\w+/g
      let href = element_href
      let rtn = href.match(re)
      console.log(rtn)
      if (rtn != null) {
        if (!(rtn.indexOf('http')) ||!(rtn.indexOf('https')) || !(rtn.indexOf('www'))) {
          return true
        }
      }
      return false
    },
    removeTargetUrlHash(){
      //検索対象のURLが#ハッシュを持っているケースがある。
      //#ハッシュを除く
      let array = this.targetUrl.split('#')
      console.log(array[0])
      return array[0] 
    }
  },
}
</script>