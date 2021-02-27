const pages = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: {
            guest: true
        }
    },
    {
        path: '/preferences',
        name: 'Preferences',
        meta: {
            requiresAuth: true
        },
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.

        component: () => import('../views/Preferences.vue')
    },

    {
        path: '/admin/users',
        name: 'Users',
        meta: {
            sidebar: true,
            requiresAuth: true,
            admin: true
        },
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.

        component: () => import('../views/admin/Users.vue')
    },
    {
        path: '/admin/logs',
        name: 'Logs',
        meta: {
            sidebar: true,
            requiresAuth: true,
            admin: true
        },
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.

        component: () => import('../views/admin/Logs.vue'),
        children: [
            {
                path: '',
                name: 'Index',
                component: () => import('../views/admin/logs/LogIndex.vue'),
            },
            {
                path: 'event-participation',
                name: 'Participation in Events',
                component: () => import('../views/admin/logs/LogEventParticipation.vue'),
            },
            {
                path: 'event-organization',
                name: 'Organization of Events',
                component: () => import('../views/admin/logs/LogEventOrganization.vue'),
            }
        ]
    },

    {
        path: '/',
        name: 'Index',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/Index.vue')
    },
    {
        path: '/forms/event-participation',
        name: 'Participation in Events',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/EventParticipation.vue')
    },
    {
        path: '/forms/event-organization',
        name: 'Organization of Events',
        meta: {
            sidebar: true,
            requiresAuth: true
        },

        component: () => import('../views/EventOrganization.vue')
    }
]

export default pages