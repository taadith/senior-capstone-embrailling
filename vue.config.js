const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      fallback: {
        path: require.resolve('path-browserify'),
        crypto: require.resolve('crypto-browserify'),
        fs: false, // Assuming 'fs' is not needed in your frontend code
        stream: require.resolve('stream-browserify') // Adding fallback for 'stream'
      }
    }
  }
});

