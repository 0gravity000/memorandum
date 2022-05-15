const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir:'../backend/dist', // npm run build 時のファイルの出力先ルート
})
