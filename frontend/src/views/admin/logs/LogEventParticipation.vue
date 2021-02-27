<template>
    <div class="log-event-participation">
        <v-data-table
                :headers="headers"
                :loading="pending"
                :items="logs"
                :items-per-page="10"
                @click:row="editItem"
                show-select
                class="elevation-1"
        >

            <template v-slot:item.title="{ item }">
                {{ item.title ? item.title : 'none' }}
            </template>

            <template v-slot:item.date="{ item }">
                {{ `${item.date_start}~${item.date_finish}` }}
            </template>

            <template v-slot:item.observations="{ item }">
                {{ item.observations ? item.observations.length > 20 ? `${item.observations.substring(0, 17)}...` :
                item.observations : 'none' }}
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
                    <v-list>
                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>User</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.user.name }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Type of Event</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.eventType }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Type of Participation</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.participationType }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item v-if="this.editedItem.title">
                            <v-list-item-content>
                                <v-list-item-title>Title</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.title }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Event</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.event }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Local</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.local }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Date</v-list-item-title>
                                <v-list-item-subtitle>{{ `${this.editedItem.date_start}~${this.editedItem.date_finish}`
                                    }}
                                </v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item v-if="this.editedItem.observations" three-line>
                            <v-list-item-content>
                                <v-list-item-title>Observations</v-list-item-title>
                                <v-list-item-subtitle>{{ this.editedItem.observations }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
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
        name: 'LogEventParticipation',
        data() {
            return {
                headers: [
                    {text: 'User', value: 'user.name'},
                    {text: 'Type of Event', value: 'eventType'},
                    {text: 'Type of Participation', value: 'participationType'},
                    {text: 'Title', value: 'title'},
                    {text: 'Event', value: 'event'},
                    {text: 'Local', value: 'local'},
                    {text: 'Date', value: 'date'},
                    {text: 'Observations', value: 'observations'}
                ],

                pending: false,
                deletePending: false,
                logs: [],

                editedIndex: -1,
                editedItem: {
                    user: {},
                    eventType: '',
                    participationType: '',
                    title: '',
                    event: '',
                    local: '',
                    date: [],
                    observations: '',
                },
                defaultItem: {
                    user: {},
                    eventType: '',
                    participationType: '',
                    title: '',
                    event: '',
                    local: '',
                    date: [],
                    observations: '',
                },

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

                fetch(`http://localhost:8000/api/forms/event-participation/list`, {
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

                fetch(`http://localhost:8000/api/forms/event-participation/${this.editedItem.id}`, requestOptions)
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
