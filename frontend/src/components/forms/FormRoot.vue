<template>
    <div :class="`log-${id}`" class="pa-4">
        <v-card elevation="2">
            <v-card-title class="mt-4 text-center justify-center py-2">
                <h4 class="text-h4">{{ name }}</h4>
            </v-card-title>

            <v-tabs
                    class="mt-4"
                    grow
            >
                <v-tabs>
                    <v-tab v-for="tab in getParentRoute.children" :key="tab.path"
                           :to="`${getParentRoute.path}/${tab.path}`">{{ tab.name }}
                    </v-tab>
                </v-tabs>
            </v-tabs>

            <v-card-text class="mt-4">

                <router-view></router-view>

            </v-card-text>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'FormRoot',
        props: {
            id: {
                type: String
            },
            name: {
                type: String
            }
        },
        computed: {
            getParentRoute() {
                const routePath = this.$route.matched[0].path;
                return this.$router.options.routes.filter(x => x.path == routePath)[0];
            }
        }
    }
</script>
