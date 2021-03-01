<template>
  <div :class="`log-${id}`">

    <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        class="m-6"
    ></v-text-field>

    <v-data-table
        :loading="pending"
        :headers="headers"
        :search="search"
        :items="logs"
        :items-per-page="10"
        :options.sync="options"
        :server-items-length="totalItems"
        @click:row="editItem"
        show-select
        class="elevation-1"
    >

      <template v-for="header in headers" v-slot:[`item.${header.value}`]="{ item }">
        <slot :name="`table.${header.value}`" v-bind:item="item">
          {{ item[header.value] }}
        </slot>
      </template>

      <template v-for="_header in headers" v-slot:[`header.${_header.value}`]="{ header }">
        <slot :name="`header.${_header.value}`" v-bind:header="header">
          {{ header.text }}
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
            DELETE
          </v-btn>

          <v-dialog v-model="dialogDelete" max-width="300">
            <v-card>
              <v-card-title class="headline">Delete this item?</v-card-title>
              <v-card-text>This action is irreversible</v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="gray" text @click="closeDelete" :disabled="deletePending">CANCEL</v-btn>
                <v-btn color="error" text @click="deleteLogConfirm" :disabled="deletePending">DELETE</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
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
    },
    userOnly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      pending: false,
      deletePending: false,

      totalItems: 0,
      options: {},

      search: '',
      searchDebounce: -1,

      logs: [],

      editedIndex: -1,
      editedItem: Object.assign({}, this.defaultItem),

      dialog: false,
      dialogDelete: false
    }
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
    dialogDelete(val) {
      val || this.closeDelete()
    },
    search(val) {
      if (val.length < 3) {
        return;
      }

      clearTimeout(this.searchDebounce)

      this.searchDebounce = setTimeout(() => {
        this.fetchLogs()
      }, 500)
    },
    options: {
      handler() {
        this.fetchLogs()
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchLogs();
  },
  methods: {
    fetchLogs() {
      this.pending = true;

      const {sortBy, sortDesc, page, itemsPerPage} = this.options

      let url = `http://localhost:8000/api/forms/${this.id}/list${this.userOnly ? '/me' : ''}?page=${page}&size=${itemsPerPage}`

      if (sortBy.length === 1 && sortDesc.length === 1) {
        url += `&sort=${sortBy[0]}&desc=${sortDesc[0]}`
      }

      if (this.search.length > 3) {
        url += `&q=${this.search}`
      }

      fetch(url, {
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
            this.totalItems = data.total;
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
      this.dialogDelete = false;

      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    deleteLog() {
      if (this.editedIndex < 0) {
        return;
      }

      this.dialogDelete = true;
    },

    deleteLogConfirm() {
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
            this.fetchLogs()
            this.close();
          })
          .catch(error => {
            console.log(error);
          })
          .finally(() => {
            this.deletePending = false
          });
    },

    closeDelete() {
      this.dialogDelete = false;
    }
  }
}
</script>
