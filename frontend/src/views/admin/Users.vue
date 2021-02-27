<template>
    <div class="admin-users pa-4">
        <v-card elevation="2">
            <v-card-title>
                Users

                <v-dialog
                        v-model="dialog"
                        max-width="500px"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                                color="primary"
                                fab
                                dark
                                outlined
                                small
                                class="ml-4"
                                v-bind="attrs"
                                v-on="on"
                        >
                            <v-icon>
                                mdi-plus
                            </v-icon>
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="headline">{{ formTitle }}</span>
                        </v-card-title>

                        <v-card-text>
                            <v-container>
                                <v-text-field
                                        v-model="editedItem.name"
                                        :disabled="editPending"
                                        label="Name"
                                ></v-text-field>
                                <v-text-field
                                        v-model="editedItem.email"
                                        :disabled="editPending"
                                        label="Email"
                                ></v-text-field>
                                <v-text-field
                                        v-if="formCreate"
                                        v-model="editedItem.password"
                                        :disabled="editPending"
                                        type="password"
                                        label="Password"
                                ></v-text-field>
                                <v-checkbox
                                        v-model="editedItem.is_superuser"
                                        :disabled="editPending"
                                        label="Admin"
                                ></v-checkbox>
                            </v-container>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                    :disabled="editPending"
                                    outlined
                                    text
                                    @click="close"
                            >
                                Cancel
                            </v-btn>
                            <v-btn
                                    color="green"
                                    :disabled="editPending"
                                    outlined
                                    text
                                    @click="save"
                            >
                                Save
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <v-spacer></v-spacer>
                <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                ></v-text-field>
            </v-card-title>

            <v-data-table
                    :headers="headers"
                    :items="users"
                    :items-per-page="10"
                    :search="search"
                    :loading="pending"

                    sort-by="name"
                    loading-text="Loading... Please wait"
            >

                <template v-slot:item.is_superuser="{ item }">
                    <v-simple-checkbox
                            v-model="item.is_superuser"
                            disabled
                    ></v-simple-checkbox>
                </template>

                <template v-slot:item.actions="{ item }">
                    <v-icon
                            small
                            class="mr-2"
                            @click="editItem(item)"
                    >
                        mdi-pencil
                    </v-icon>
                    <v-icon
                            small
                            @click="deleteItem(item)"
                    >
                        mdi-delete
                    </v-icon>

                    <v-dialog v-model="dialogDelete" max-width="300">
                        <v-card>
                            <v-card-title class="headline">Delete this item?</v-card-title>
                            <v-card-text>This action is irreversible</v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="gray" text @click="closeDelete" :disabled="deletePending">CANCEL</v-btn>
                                <v-btn color="error" text @click="deleteItemConfirm" :disabled="deletePending">DELETE</v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </template>

            </v-data-table>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'Users',
        data() {
            return {
                headers: [
                    {text: 'Name', value: 'name'},
                    {text: 'Email', value: 'email'},
                    {text: 'Admin', value: 'is_superuser'},
                    {text: 'Actions', value: 'actions', sortable: false},
                ],
                users: [],
                search: '',

                editedIndex: -1,
                editedItem: {
                    name: '',
                    email: '',
                    password: '',
                    is_superuser: false
                },
                defaultItem: {
                    name: '',
                    email: '',
                    password: '',
                    is_superuser: false
                },

                pending: true,
                editPending: false,
                deletePending: false,

                dialog: false,

                dialogDelete: false,
            }
        },
        mounted() {
            this.fetchUsers();
        },
        watch: {
            dialog(val) {
                val || this.close()
            },
            dialogDelete(val) {
                val || this.closeDelete()
            },
        },
        computed: {
            formCreate() {
                return this.editedIndex === -1;
            },
            formTitle() {
                return this.formCreate ? 'New Item' : 'Edit Item'
            }
        },
        methods: {
            fetchUsers() {
                this.pending = true;

                fetch(`http://localhost:8000/api/users/list`, {
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

                        this.users = data.users;
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.pending = false
                    });
            },

            deleteItem(item) {
                this.editedIndex = this.users.indexOf(item)
                this.editedItem = Object.assign({}, item)

                this.dialogDelete = true
            },

            deleteItemConfirm() {
                let requestOptions = {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    },

                };

                this.deletePending = true;

                fetch(`http://localhost:8000/api/users/${this.editedItem.id}`, requestOptions)
                    .then(async response => {
                        if (!response.ok) {
                            return Promise.reject(response.status);
                        }

                        this.users.splice(this.editedIndex, 1)
                        this.closeDelete();
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.deletePending = false
                    });

            },

            closeDelete() {
                this.dialogDelete = false
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem)
                    this.editedIndex = -1
                })
            },

            editItem(item) {
                this.editedIndex = this.users.indexOf(item)
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

            save() {
                let requestOptions = {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    }
                };

                let url = '';

                if (this.formCreate) {
                    url = `http://localhost:8000/api/users/create`
                    requestOptions['method'] = 'POST';

                    let body = Object.assign({}, this.editedItem);

                    requestOptions['body'] = JSON.stringify(body)
                } else {
                    url = `http://localhost:8000/api/users/${this.editedItem.id}`
                    requestOptions['method'] = 'PATCH';

                    let body = Object.assign({}, this.editedItem);
                    delete body.password;

                    requestOptions['body'] = JSON.stringify(body)
                }

                this.editPending = true;

                fetch(url, requestOptions)
                    .then(async response => {
                        const data = await response.json();

                        // check for error response
                        if (!response.ok) {
                            // get error message from body or default to response status
                            const error = (data && data.detail) || response.status;
                            return Promise.reject(error);
                        }

                        if (this.editedIndex >= 0) {
                            this.users.splice(this.editedIndex, 1)
                        }

                        this.users.push(data);
                        this.close();
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.editPending = false
                    });
            }
        }
    }
</script>
