module.exports = {
    transpileDependencies: [
        'vuetify'
    ],
    devServer: {
        port: 8080,
        proxy: {
            '^/api': {
                target: 'http://localhost:8000',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    //'^/api': ''
                }
            },
        }
    }
}
