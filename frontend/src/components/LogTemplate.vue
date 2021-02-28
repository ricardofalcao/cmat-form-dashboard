<template>
  <div :class="`log-${id}`">

    <v-data-table
        :loading="pending"
        :headers="headers"
        :items="logs"
        :items-per-page="10"
        @click:row="editItem"
        show-select
        class="elevation-1"
    >

      <template v-for="header in headers" v-slot:[`item.${header.value}`]="{ item }">
        <slot :name="`table.${header.value}`" v-bind:item="item">
          {{ item[header.value] }}
        </slot>
      </template>

    </v-data-table>

    <v-dialog
        v-model="dialog"
        max-width="500px"
    >
      <v-card>
        <v-card-title>
        </v-card-title>

        <v-card-text>
          <slot name="dialog" :item="editedItem">
          </slot>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              @click="deleteLog"
              :disabled="deletePending"
              color="gray"
              text
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script>
export default {
  name: 'LogTemplate',
  props: {
    id: {
      type: String
    },
    headers: {
      type: Array
    },
    defaultItem: {
      type: Object
    }
  },
  data() {
    return {
      pending: false,
      deletePending: false,

      logs: [],

      editedIndex: -1,
      editedItem: Object.assign({}, this.defaultItem),

      dialog: false
    }
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
  },
  mounted() {
    this.fetchLogs();
  },
  methods: {
    fetchLogs() {
      this.pending = true;

      fetch(`http://localhost:8000/api/forms/${ this.id }/list`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
          'Content-Type': 'application/json',
        }
      })
          .then(async response => {
            const data = await response.json();

            // check for error response
            if (!response.ok) {
              // get error message from body or default to response status
              const error = (data && data.detail) || response.status;
              return Promise.reject(error);
            }

            this.logs = data.forms;
          })
          .catch(error => {
            console.log(error);
          })
          .finally(() => {
            this.pending = false
          });
    },

    editItem(row, value) {
      const item = value.item;
      this.editedIndex = this.logs.indexOf(item)
      this.editedItem = Object.assign({}, item)

      this.dialog = true
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    deleteLog() {
      if (this.editedIndex < 0) {
        return;
      }

      let requestOptions = {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
          'Content-Type': 'application/json',
        },

      };

      this.deletePending = true;

      fetch(`http://localhost:8000/api/forms/${this.id}/${this.editedItem.id}`, requestOptions)
          .then(async response => {
            if (!response.ok) {
              return Promise.reject(response.status);
            }

            this.logs.splice(this.editedIndex, 1)
            this.close();
          })
          .catch(error => {
            console.log(error);
          })
          .finally(() => {
            this.deletePending = false
          });
    },
  }
}
</script>
