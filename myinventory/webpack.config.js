const path = require('path');

module.exports = {
  entry: './frontend/index.js',
  output: {
    filename: 'index-bundle.js',
    path: path.resolve(__dirname, './static'),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: [
            "@babel/preset-env", 
            "@babel/preset-react"
          ]
        }
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ]
  }
};
