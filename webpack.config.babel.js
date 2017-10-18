import webpack from 'webpack';
import path from 'path';
// import HtmlWebpackPlugin from 'html-webpack-plugin';
var BundleTracker = require('webpack-bundle-tracker');

import WriteFilePlugin from 'write-file-webpack-plugin';



const LAUNCH_COMMAND = process.env.npm_lifecycle_event;

const isProduction = LAUNCH_COMMAND === 'production';
process.env.BABEL_ENV = LAUNCH_COMMAND;

const PATHS = {
    src  : path.join(__dirname, 'rookie_booking/react-redux/src'),
    build: path.join(__dirname, 'rookie_booking/static/js/react')
};

// const HTMLWebpackPluginConfig = new HtmlWebpackPlugin({
//     template: './templates/base.html',
//     filename: 'base.html',
//     // template: `${PATHS.app}/index.html`,
//     // filename: 'index.html',
//     inject  : 'body'
// });

const productionPlugin = new webpack.DefinePlugin({
    'process.env': {
        NODE_ENV: JSON.stringify('production')
    }
});

const base = {
    entry: [
        './rookie_booking/react-redux/src/index.js'
    ],
    output: {
        path    : PATHS.build,
        // filename: 'index_bundle.js'
        filename : '[name]-[hash].js',
        // publicPath: 'http://localhost:8080/js/react/'
    },
    module: {
        loaders: [
            { test: /\.js$/, exclude: /node_modules/, loader: ['react-hot-loader/webpack', 'babel-loader'] },
            { test: /\.css$/, loader: 'style-loader!css-loader?sourceMap&modules&localIdentName=[name]__[local]___[hash:base64:5]' },
            {
                test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
                use : {
                    loader : 'url-loader',
                    options: {
                        limit: 100000
                    }
                }
            }
        ]
    },
    resolve: {
        modules: [path.resolve('./rookie_booking/react-redux/src'), 'node_modules']
    }
};

const developmentConfig = {
    devtool  : 'cheap-module-inline-source-map',
    devServer: {
        historyApiFallback: true,
        contentBase: PATHS.build,
        hot        : false,
        inline     : true
    },
    plugins: [
        new WriteFilePlugin(),
        // HTMLWebpackPluginConfig,
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.HotModuleReplacementPlugin()
    ]
};

const productionConfig = {
    devtool: 'cheap-module-source-map',
    plugins: [productionPlugin, new BundleTracker({filename: './webpack-stats-prod.json'}),]
};

export default Object.assign({}, base, isProduction === true ? productionConfig : developmentConfig);
