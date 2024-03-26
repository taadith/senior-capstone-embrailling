const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: 'The Embrailler',
    },
  },
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

