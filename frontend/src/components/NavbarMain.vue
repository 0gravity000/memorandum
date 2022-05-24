<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/">
      <a class="navbar-brand">MemoRandum</a>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/auth/register">
              <a class="nav-link">ユーザー登録</a>
            </router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/auth/login">
              <a class="nav-link">ログイン</a>
            </router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/about">
              <a class="nav-link">About</a>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavbarMain',
  props: {
  },
  data () {
    return {
    }
  },
  updateed () {
  },
  mounted () {
  },
  methods: {
  },
  computed: {
    //vuexで状態管理を試みるが、リロードでstateがクリアされることが判明
    //コンポーネント間の親子受け渡しで実装する
    /*
    showAuthUser () {
      return this.$store.state.authEmail
    }
    */
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
