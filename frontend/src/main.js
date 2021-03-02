import Vue from 'vue'

import App from './App.vue'
import './assets/index.scss'

import router from './router'
import store from './store'

import vuetify from './plugins/vuetify';

Vue.config.productionTip = false


router.beforeEach((to, from, next) => {
    let accessToken = localStorage.getItem('jwt');

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (accessToken == null) {
            next({
                path: '/login',
                params: {nextUrl: to.fullPath}
            })
        } else {
            fetch(`${Vue.prototype.$apiUrl}/users/me`, {
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                    'Content-Type': 'application/json'
                }
            })
                .then(async response => {
                    const user = await response.json();

                    // check for error response
                    if (!response.ok) {
                        // get error message from body or default to response status
                        const error = (user && user.detail) || response.status;
                        return Promise.reject(error);
                    }

                    store.commit('setUser', user);

                    if (to.matched.some(record => record.meta.admin)) {
                        if (user.is_superuser) {
                            next()
                        } else {
                            next({name: '/'})
                        }
                    } else {
                        next()
                    }
                })
                .catch(error => {
                    console.log(error);

                    localStorage.removeItem('jwt');

                    next({path: '/login'})
                });
        }
    } else if (to.matched.some(record => record.meta.guest)) {
        if (accessToken == null) {
            next()
        } else {
            next({path: '/'})
        }
    } else {
        next()
    }
})

Vue.prototype.$apiUrl = process.env.API_URL

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')
