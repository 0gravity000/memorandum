<template>
  <div class="sidebar-home">
    <ul class="list-group list-group-flush">
      <li class="list-group-item">
        <router-link to="/dom-experiment-01">DOM実験01</router-link>
      </li>
      <li class="list-group-item">
        <router-link to="/bookmarks">ブックマーク一覧</router-link>
      </li>
      <li class="list-group-item">
        <router-link to="/bookmarks-import">Chromeブックマークインポート</router-link>
      </li>
      <!--       
      <li class="list-group-item">
      <details>
      <summary>xxx</summary>
        <li class="list-group-item">
          <router-link to="/closures-experiment-01">xxx</router-link>
        </li>
      </details>
      </li>
       -->
    </ul>
  </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  padding-left: 1rem;
}
</style>
