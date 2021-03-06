<template>
    <div :class="`log-${id}`">

        <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                prepend-icon="mdi-filter-variant"
                label="Filter"
                single-line
                hide-details
                class="ma-6"
        ></v-text-field>

        <v-menu
                v-if="dateSearch"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-text-field
                        class="ma-6"
                        :value="formatDate"
                        prepend-icon="mdi-calendar"
                        append-icon="mdi-close"
                        @click:append="dateSearchValue = []"
                        label="Filter Date"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                ></v-text-field>
            </template>
            <v-date-picker
                    v-model="dateSearchValue"
                    range
            ></v-date-picker>
        </v-menu>

        <v-data-table
                :loading="pending"
                :headers="headers"
                :search="search"
                :items="logs"
                :items-per-page="10"
                :options.sync="options"
                :server-items-length="totalItems"
                v-model="selectedLogs"
                @click:row="editItem"
                show-select
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

            <template #footer>
                <v-menu offset-y>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                                v-if="schemas.length > 0"

                                class="ma-4"
                                color="primary"
                                outlined

                                v-bind="attrs"
                                v-on="on"
                        >
                            EXPORT SELECTED
                        </v-btn>
                    </template>
                    <v-list v-if="schemas.length > 0">
                        <v-list-item
                                v-for="(schema, index) in schemas"
                                :key="index"

                                @click="exportSchema(schema)"
                        >
                            <v-list-item-title>{{ schema.name }}</v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
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
                    <v-form v-model="valid">
                        <slot name="dialog" :item="editedItem"></slot>
                    </v-form>
                </v-card-text>

                <v-card-actions>
                    <v-btn
                            @click="deleteLog"
                            :disabled="deletePending"
                            color="red"
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
                                <v-btn color="error" text @click="deleteLogConfirm" :disabled="deletePending">DELETE
                                </v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                    <v-spacer></v-spacer>

                    <v-btn
                            text
                            @click="close"
                    >
                        CANCEL
                    </v-btn>

                    <v-btn
                            color="green"
                            text
                            :disabled="editPending"
                            @click="save"
                    >
                        SAVE
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <div v-if="showSchemas">
            <v-card-title>
                Schemas

                <v-dialog
                        v-model="dialogSchema"
                        fullscreen
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
                            <span class="headline">{{ schemaFormTitle }}</span>
                        </v-card-title>

                        <v-card-text>
                            <v-form v-model="schemaValid">
                                <v-text-field
                                        v-model="schemaItem.name"
                                        :disabled="schemasPending"
                                        label="Name"
                                ></v-text-field>

                                <v-textarea
                                        v-model="schemaItem.template"
                                        solo
                                        auto-grow

                                        label="Template"
                                ></v-textarea>

                                <v-select
                                        :items="[
                                            { name: 'Text', extension: 'txt' },
                                            { name: 'Latex', extension: 'tex' },
                                            { name: 'CSV', extension: 'csv' },
                                        ]"
                                        item-text="name"
                                        item-value="extension"
                                        v-model="schemaItem.extension"

                                        label="Extension"
                                ></v-select>

                                <template v-if="schemaVars.length > 0">
                                    <v-list dense>
                                        <v-subheader>VARIABLES (More information <a target="_blank" href="https://handlebarsjs.com/guide/builtin-helpers.html" class="ml-1">here</a>) </v-subheader>

                                        <v-flex>
                                            <v-row>
                                                <v-col v-for="(svar, index) in schemaVars" :key="index">
                                                    <v-list-item>
                                                        <v-list-item-content>
                                                            <v-list-item-title>{{ svar.title }}</v-list-item-title>
                                                            <v-list-item-subtitle>{{ svar.description }}
                                                            </v-list-item-subtitle>
                                                        </v-list-item-content>
                                                    </v-list-item>
                                                </v-col>
                                            </v-row>
                                        </v-flex>
                                    </v-list>
                                </template>
                            </v-form>
                        </v-card-text>

                        <v-card-actions>
                            <v-btn
                                    v-if="schemaIndex >= 0"
                                    color="red"
                                    :disabled="schemasPending"
                                    text
                                    @click="deleteSchema"
                            >
                                DELETE
                            </v-btn>
                            <v-dialog v-model="dialogDeleteSchema" max-width="300">
                                <v-card>
                                    <v-card-title class="headline">Delete this item?</v-card-title>
                                    <v-card-text>This action is irreversible</v-card-text>
                                    <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn color="gray" text @click="closeDeleteSchema"
                                               :disabled="schemasDeletePending">CANCEL
                                        </v-btn>
                                        <v-btn color="error" text @click="deleteSchemaConfirm"
                                               :disabled="schemasDeletePending">
                                            DELETE
                                        </v-btn>
                                        <v-spacer></v-spacer>
                                    </v-card-actions>
                                </v-card>
                            </v-dialog>

                            <v-spacer></v-spacer>
                            <v-btn
                                    :disabled="schemasPending"
                                    text
                                    @click="closeSchema"
                            >
                                CANCEL
                            </v-btn>

                            <v-btn
                                    color="green"
                                    :disabled="schemasPending"
                                    text
                                    @click="saveSchema"
                            >
                                SAVE
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-card-title>

            <v-data-table
                    :loading="schemasPending"
                    :headers="schemasHeaders"
                    :items="schemas"
                    :items-per-page="10"
                    @click:row="editSchema"
            >

                <template #item.template="{item}">
                    {{ item.template.length > 60 ? `${item.template.substring(0, 57)}...` : item.template }}
                </template>
            </v-data-table>
        </div>
    </div>
</template>

<script>
    const Handlebars = require("handlebars");

    import cloneDeep from 'clone-deep'

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
            },
            preprocessInbound: {
                type: Function,
                default: (val) => {
                    return val
                }
            },
            preprocessOutbound: {
                type: Function,
                default: (val) => {
                    return val
                }
            },
            dateSearch: {
                type: Boolean,
                default: false
            },
            showSchemas: {
                type: Boolean,
                default: true
            },
            schemaVars: {
                type: Array,
                default: () => []
            }
        },
        data() {
            const _defaultSchemaItem = {
                id: '',
                user: {},
                name: '',
                template: '',
                extension: 'txt'
            }

            return {
                schemasHeaders: [
                    {text: 'Name', value: 'name'},
                    {text: 'Template', value: 'template'}
                ],

                valid: false,
                schemaValid: false,

                pending: false,
                schemasPending: false,
                schemasDeletePending: false,

                editPending: false,
                deletePending: false,

                totalItems: 0,
                options: {},

                search: '',
                dateSearchValue: [],
                searchDebounce: -1,

                logs: [],
                selectedLogs: [],
                schemas: [],

                editedIndex: -1,
                editedItem: cloneDeep(this.defaultItem),

                schemaIndex: -1,
                schemaItem: cloneDeep(_defaultSchemaItem),
                defaultSchemaItem: _defaultSchemaItem,

                dialog: false,
                dialogDelete: false,
                dialogSchema: false,
                dialogDeleteSchema: false,
            }
        },
        watch: {
            dialog(val) {
                val || this.close()
            },
            dialogDelete(val) {
                val || this.closeDelete()
            },
            dialogSchema(val) {
                val || this.closeSchema()
            },
            dialogDeleteSchema(val) {
                val || this.closeDeleteSchema()
            },
            search(val) {
                if (val.length < 3) {
                    return;
                }

                clearTimeout(this.searchDebounce)

                this.searchDebounce = setTimeout(() => {
                    this.fetchLogs()
                }, 300)
            },
            dateSearchValue(val) {
                if (val.length == 1) {
                    return;
                }

                this.fetchLogs()
            },
            options: {
                handler() {
                    this.fetchLogs()
                },
                deep: true,
            },
        },
        computed: {
            formatDate() {
                return this.dateSearchValue.join(' ~ ')
            },
            schemaFormTitle() {
                return this.schemaIndex < 0 ? 'Create schema' : 'Edit schema'
            }
        },
        async mounted() {
            this.fetchSchemas();
            this.fetchLogs();
        },
        methods: {
            fetchSchemas() {
                if (!this.showSchemas) {
                    return;
                }

                this.schemasPending = true;

                fetch(`${this.$apiUrl}/forms/${this.id}/exports/list`, {
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

                        this.schemas = data.schemas;
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.schemasPending = false
                    });
            },
            fetchLogs() {
                this.pending = true;

                const {sortBy, sortDesc, page, itemsPerPage} = this.options

                let url = `${this.$apiUrl}/forms/${this.id}/list${this.userOnly ? '/me' : ''}?page=${page}&size=${itemsPerPage}`

                if (sortBy.length === 1 && sortDesc.length === 1) {
                    url += `&sort=${sortBy[0]}&desc=${sortDesc[0]}`
                }

                if (this.search.length > 3) {
                    url += `&q=${this.search}`
                }

                if (this.dateSearch && this.dateSearchValue.length == 2) {
                    url += `&date_from=${this.dateSearchValue[0]}&date_to=${this.dateSearchValue[1]}`
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

                        this.logs = data.forms.map(v => this.preprocessInbound(v));
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
                this.editedItem = cloneDeep(item)

                this.dialog = true
            },

            save() {
                if (!this.valid) {
                    return;
                }

                this.editPending = true;

                fetch(`${this.$apiUrl}/forms/${this.id}/${this.editedItem.id}`, {
                    method: "PATCH",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.preprocessOutbound(this.editedItem))
                })
                    .then(async response => {
                        const data = await response.json();

                        // check for error response
                        if (!response.ok) {
                            // get error message from body or default to response status
                            const error = (data && data.detail) || response.status;
                            return Promise.reject(error);
                        }

                        this.logs[this.editedIndex] = Object.assign(this.logs[this.editedIndex], this.preprocessInbound(data));
                        this.close();
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.editPending = false
                    });
            },

            close() {
                this.dialog = false
                this.dialogDelete = false;

                this.$nextTick(() => {
                    this.editedItem = cloneDeep(this.defaultItem)
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

                fetch(`${this.$apiUrl}/forms/${this.id}/${this.editedItem.id}`, requestOptions)
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
            },

            createSchema() {
                this.dialogSchema = true;
            },

            editSchema(item) {
                this.schemaIndex = this.schemas.indexOf(item)
                this.schemaItem = Object.assign({}, item)

                this.dialogSchema = true
            },

            saveSchema() {
                if (!this.schemaValid) {
                    return;
                }

                let requestOptions = {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    }
                };

                let url = '';

                if (this.schemaIndex < 0) {
                    url = `${this.$apiUrl}/forms/${this.id}/exports`
                    requestOptions['method'] = 'POST';

                    let body = Object.assign({}, this.schemaItem);
                    requestOptions['body'] = JSON.stringify(body)
                } else {
                    url = `${this.$apiUrl}/forms/${this.id}/exports/${this.schemaItem.id}`
                    requestOptions['method'] = 'PATCH';

                    let body = Object.assign({}, this.schemaItem);
                    requestOptions['body'] = JSON.stringify(body)
                }

                this.schemasPending = true;

                fetch(url, requestOptions)
                    .then(async response => {
                        const data = await response.json();

                        // check for error response
                        if (!response.ok) {
                            // get error message from body or default to response status
                            const error = (data && data.detail) || response.status;
                            return Promise.reject(error);
                        }

                        if (this.schemaIndex >= 0) {
                            this.schemas[this.schemaIndex] = Object.assign(this.schemas[this.schemaIndex], data);
                        } else {
                            this.schemas.push(data)
                        }

                        this.closeSchema();
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.schemasPending = false
                    });
            },

            closeSchema() {
                this.dialogSchema = false
                this.dialogDeleteSchema = false;

                this.$nextTick(() => {
                    this.schemaItem = cloneDeep(this.defaultSchemaItem)
                    this.schemaIndex = -1
                })
            },

            deleteSchema() {
                this.dialogDeleteSchema = true
            },

            deleteSchemaConfirm() {
                let requestOptions = {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    },

                };

                this.schemasDeletePending = true;

                fetch(`${this.$apiUrl}/forms/${this.id}/exports/${this.schemaItem.id}`, requestOptions)
                    .then(async response => {
                        if (!response.ok) {
                            return Promise.reject(response.status);
                        }

                        this.schemas.splice(this.schemaIndex, 1)
                        this.fetchSchemas()
                        this.closeSchema();
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.schemasDeletePending = false
                    });
            },

            closeDeleteSchema() {
                this.dialogDeleteSchema = false;
            },

            exportSchema(schema) {
                if (this.selectedLogs.length <= 0) {
                    return;
                }

                const template = Handlebars.compile(schema.template);
                const text = template({
                    items: this.selectedLogs
                })

                var element = document.createElement('a');
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
                element.setAttribute('download', `Export.${schema.extension}`);

                element.style.display = 'none';
                document.body.appendChild(element);

                element.click();

                document.body.removeChild(element);
            }
        }
    }
</script>
