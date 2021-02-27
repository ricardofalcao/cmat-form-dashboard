<template>
    <div class="admin-logs pa-4">
        <v-card elevation="2">
            <v-card-title>
                Logs
            </v-card-title>

            <v-tabs>
                <v-tab v-for="tab in getParentRoute.children" :key="tab.path" :to="`${getParentRoute.path}/${tab.path}`">{{ tab.name }}
                </v-tab>
            </v-tabs>

            <router-view></router-view>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'Logs',
        data() {
            return {}
        },
        computed: {
            getParentRoute() {
                const routePath = this.$route.matched[0].path;
                return this.$router.options.routes.filter(x => x.path == routePath)[0];
            }
        }
    }
</script>
