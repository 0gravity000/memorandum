<template>
  <div class="bookmarks-index">
    <p>{{authUser.email}}&nbsp;さん
      <a href="#" @click="authLogout">ログアウト</a>
    </p>
    <h2>ブックマーク一覧</h2>
    <router-link to="/bookmarks/create">ブックマーク登録</router-link>&nbsp;
    <router-link to="/tags">タグ一覧</router-link>&nbsp;
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
    フィルタータグ
    <div class="row">
      <div class="col">
        <span v-for="tag in tags" :key="tag">
          <span :class="{'filtered-tag': isFilteredThisTag(tag.id)}" @click="toggledTagItem(tag.id)">
            &nbsp;{{tag.name}}&nbsp;
          </span>
        </span>
      </div>
    </div>
    <!-- {{bookmarks}}<br> -->
    <div v-for="bookmark in bookmarks" :key="bookmark">
      <!-- このブックマークが持つタグがフィルタされているかチェック -->
      <div v-show="shouldDisplayThisBookmark(bookmark.id)">
      <!-- 
      <div>
       -->
        <div class="card me-3">
          <div class="card-body">
            <span v-for="i in bookmark.importance" :key="i">{{"★"}}&nbsp;</span>
            <span v-for="bookmarkstag in bookmark_tags" :key="bookmarkstag">
              <!-- このブックマークが持つタグを表示 -->
              <span v-show="bookmarkstag.bookmark_id == bookmark.id">
                {{tagidToTagname(bookmarkstag.tag_id)}}&nbsp;
                <!-- 
                {{bookmarkstag.tag_id}}&nbsp;
                -->
              </span>
            </span>
            <!-- 
            <h6 class="card-subtitle mb-2 text-muted fw-light">{{bookmark.id}}</h6>
            <h5 class="card-title" data-bs-toggle="tooltip" :title="bookmark.remarks">{{bookmark.title}}</h5>
            -->
            <h5 class="card-title">{{bookmark.title}}</h5>
            <h6 class="card-subtitle mb-2 fw-light">{{bookmark.remarks}}</h6>
            <a :href="bookmark.url" target="_blank" rel="noopener noreferrer">
              <p class="card-text">{{bookmark.url}}</p>
            </a>
          <router-link :to="{name: 'bookmarks-update', params: {id: bookmark.id}}">編集</router-link>&nbsp;
          <a href="" @click="deleteBookmarks(bookmark.id)">削除</a>
          </div>
        </div>
      </div>
    </div>
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
      bookmarks: [],
      sortItem: "",
      sortAsc: "",
      tags: [],
      bookmark_tags: [],
      filteredTags: [],
    }
  },
  mounted() {
    this.showBookmarks(this.sortItem, this.sortAsc)
    console.log("mounted exec this.showBookmarks() ")
  },
  computed: {
  },
  methods: {
    shouldDisplayThisBookmark(bookmark_id) {
      //filteredTagsが空の場合は全ブックマークを表示
      if (this.filteredTags == "") {
        console.log("filteredTags は空")
        return true
      } else {
        let isHit = false
        for(let i=0; i < this.bookmark_tags.length; i++) {
          //該当のブックマークかチェック
          if (this.bookmark_tags[i].bookmark_id == bookmark_id) {
            for(let k=0; k < this.filteredTags.length; k++) {
              console.log(bookmark_id)
              if(this.bookmark_tags[i].tag_id == this.filteredTags[k]){
                console.log(this.filteredTags[k])
                isHit = true
                return true
              }
            }
          }
        }
        //配列に存在しない場合、false
        if (isHit == false) {
          console.log("該当なし")
          return false
        }
      }
    },
    isFilteredThisTag(tag_id) {
      let isHit = false
      for(let i=0; i < this.filteredTags.length; i++) {
        //配列に存在する場合、trueを返す
        //console.log(this.tags[i].id)
        if (this.filteredTags[i] == tag_id) {
          isHit = true
          return true
        }
      }
      //配列に存在しない場合、false
      if (isHit == false) {
        return false
      }
    },
    toggledTagItem(tag_id) {
      //console.log(tag_id)
      let isHit = false
      for(let i=0; i < this.filteredTags.length; i++) {
        //配列に存在する場合、削除
        //console.log(this.tags[i].id)
        if (this.filteredTags[i] == tag_id) {
          this.filteredTags.splice(i, 1) 
          isHit = true
          console.log(this.filteredTags)
        }
      }
      //配列に存在しない場合、追加
      if (isHit == false) {
        this.filteredTags.push(tag_id)
        console.log(this.filteredTags)
      }
    },
    tagidToTagname(tag_id) {
      //console.log(tag_id)
      for(let i=0; i < this.tags.length; i++) {
        //console.log(this.tags[i].id)
        if (this.tags[i].id == tag_id) {
          return this.tags[i].name
        }
      }
    },
    confirmDelete() {
      return confirm("ブックマークを削除します")
    },
    authLogout: function(){
      let self = this;  //promiseコールバック関数内でthisは使えないので回避用 this.$router.push('/')
      axios.get('/api/auth/logout')
      .then(function (res) {
        console.log(res.data)
        let resdate = {email: "ゲスト"}
        self.$emit('update-auth-notification', resdate)
        //self.$store.commit('clearAuthUser')  //vuexのstateで管理
      })
      .catch(function (err){
        console.log(err)
      })
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
        self.tags = res.data[3]
        self.bookmark_tags = res.data[4]
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

<style scoped>
  .filtered-tag {
    font-weight: bold;
    border-style: solid;
  }
</style>