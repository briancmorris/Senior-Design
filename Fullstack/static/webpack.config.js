const webpack = require('webpack');
const config = {
    entry:  __dirname + '/js/index.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
      rules: [
        {
          test: /\.jsx?/,
          exclude: /node_modules/,
          use: 'babel-loader'
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: "style-loader",
              options: {
                sourceMap: true,
              }
            },
            {
              loader: "css-loader",
              options: {
                sourceMap: true,
                modules: true,
                localIdentName: "[local]___[hash:base64:5]"
              }
            }
          ]
        }
        // {
        //   test: /\.css$/,
        //   loaders: [
        //     'style-loader?sourceMap',
        //     'css-loader?modules&importLoaders=1&localIdentName=[path]___[name]__[local]___[hash:base64:5]'
        //   ],
        //   // use: [ 'style-loader', 'css-loader' ],
        // }
      ]
    }
};
module.exports = config;