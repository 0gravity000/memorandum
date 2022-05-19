<template>
  <div class="bookmarks-import">
    <h2>ブックマークインポート</h2>
    <p>Google Chromeのブックマークを選択してください</p>
    <label v-show="!uploadedBookmark" class="input-item_label">
      <input type="file" @change="onFileChange" />
    </label>
    
    <div v-show="uploadedBookmark" class="preview-item-btn" @click="remove">
      <p class="preview-item-name">{{ file_name }}</p>
      <div class="preview-item-icon">close</div>
    </div>
    <div class="preview-area">
      <!-- 
      <div v-html="uploadedBookmark"></div>
      {{uploadedBookmark}}
      <button type="button" v-show="uploadedBookmark">整形</button>
      <img
        v-show="uploadedBookmark"
        class="preview-item-file"
        :src="uploadedBookmark"
        alt=""
      />
     -->
    </div>
    <div v-for="element in elements" :key="element" class="mt-3">
      <!-- 
      {{element}}
       -->
      <div v-if="element.name == 'a'">
        <div :title="element.txt" @click="createBookmark(element)">{{element.txt}}</div>
        <a :href="element.href" target="_blank" rel="noopener noreferrer">
          {{element.href}}
        </a>
      </div>
      <div v-else>
        <h3>{{element.txt}}</h3> 
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
      file_name: '',
      beforeBookmark: '',
      uploadedBookmark: '',
      elements: [],
      //element:{},
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
    onFileChange(e) {
      const files = e.target.files || e.dataTransfer.files
      console.log(files)
      this.createBlob(files[0]);
      this.file_name = files[0].name;
    },
    // アップロードしたファイルを表示
    createBlob(file) {
      const reader = new FileReader();
      reader.readAsText(file)
      reader.onload = e => {
        const tempEl = document.createElement('div')
        tempEl.innerHTML = e.target.result //html要素に変換
        this.beforeBookmark = tempEl.innerHTML
        //const div = document.querySelector('.preview-area')
        //div.innerHTML = e.target.result //html要素に変換
        //this.beforeBookmark = div.innerHTML
        this.adjustBookmark()
        //this.uploadedBookmark = div.innerHTML
        /*
        const div = document.createElement('div');
        div.innerHTML = e.target.result //html要素に変換
        this.uploadedBookmark = div.innerHTML
        */
        //this.uploadedBookmark = e.target.result;
      }
      /*
      fetch(file)
        .then(response => response.text())
        .then(text => this.uploadedBookmark = text)
      */
      //reader.readAsDataURL(file);
    },
    adjustBookmark() {
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/adjustBookmark', {
        beforeBookmark: self.beforeBookmark,
      })
      .then(function (res) {
        console.log(res.data)
        self.elements = res.data
      })
      .catch(function (err){
        console.log(err)
      })
    },
    createBookmark: function(element){
      //let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.post('/api/bookmarks', {
        title: element.txt,
        url: element.href,
        remarks: "",
      })
      .then(function (res) {
        console.log(res.data)
        //self.$router.push({name: "bookmarks-index"})
      })
      .catch(function (err){
        console.log(err)
      })
    },
    remove() {
      this.uploadedBookmark = false;
    },
  },
}
</script>