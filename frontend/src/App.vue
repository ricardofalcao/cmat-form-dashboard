<template>
  <v-app>
    <div v-if="this.$router.currentRoute.path == '/login'">
      <router-view/>
    </div>

    <div v-else>
      <v-navigation-drawer
          v-model="drawer"
          app
      >
        <v-list dense>
          <v-list-item
              v-for="page in getUserPages"
              :key="page.path"
              :to="page.path"
          >
            <!--<v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>-->

            <v-list-item-content>
              {{ page.name }}
            </v-list-item-content>

          </v-list-item>
        </v-list>

        <v-divider v-if="hasAdminPages"/>

        <v-list dense>
          <v-list-item
              v-for="page in getAdminPages"
              :key="page.path"
              :to="page.path"
          >
            <!--<v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>-->

            <v-list-item-content>
              {{ page.name }}
            </v-list-item-content>
          </v-list-item>
        </v-list>

      </v-navigation-drawer>

      <v-app-bar app dark>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

        <v-toolbar-title>CMAT Indicators</v-toolbar-title>

        <v-spacer></v-spacer>

        <div>
          Logged in as <span>{{ getUser.name }}</span>
        </div>

        <v-btn to="/preferences" icon>
          <v-icon>mdi-cog-outline</v-icon>
        </v-btn>

        <v-btn @click="logout">
          Logout
        </v-btn>
      </v-app-bar>

      <v-main>
        <router-view/>
      </v-main>
    </div>
  </v-app>
</template>

<script>
import {pages} from '@/utils/constants'

export default {
  name: 'App',
  data() {
    return {
      drawer: true
    }
  },
  computed: {
    getUserPages() {
      return pages.filter(p => p.meta.sidebar && !p.meta.admin);
    },
    getAdminPages() {
      const user = this.$store.state.user;
      return user.is_superuser ? pages.filter(p => p.meta.sidebar && p.meta.admin) : [];
    },
    hasAdminPages() {
      return this.getAdminPages.length > 0;
    },
    getUser() {
      return this.$store.state.user;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('jwt');

      this.$router.push('/login')
    }
  }
}
</script>