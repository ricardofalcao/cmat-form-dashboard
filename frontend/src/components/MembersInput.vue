<template>
    <div class="members-input">
        <v-autocomplete
                :value="members"
                @input="updateMembers($event)"

                :items="entries"

                clearable
                chips
                deletable-chips

                :search-input.sync="search"

                :label="label"

                item-text="name"
                item-value="name"

                multiple
                auto-select-first
                return-object
        >

            <template v-slot:selection="data">
                <v-chip
                        v-bind="data.attrs"
                        :input-value="data.selected"
                        close
                        @click="data.select"
                        @click:close="removeMember(data.item)"
                >
                    {{ data.item.name }}
                </v-chip>
            </template>

            <template v-slot:item="data">
                <template v-if="typeof data.item !== 'object'">
                    <v-list-item-content v-text="data.item"></v-list-item-content>
                </template>
                <template v-else>
                    <v-list-item-content>
                        <v-list-item-title v-html="data.item.name"></v-list-item-title>
                        <v-list-item-subtitle v-html="data.item.email"></v-list-item-subtitle>
                    </v-list-item-content>
                </template>
            </template>

        </v-autocomplete>
    </div>
</template>

<script>
    export default {
        name: "MembersInput",
        components: {},
        props: {
            members: Array,
            label: {
                type: String,
                default: ''
            }
        },
        data() {
            return {
                search: null,

                pending: false,
                entries: [],
            }
        },
        methods: {
            removeMember(member) {
                const index = this.members.indexOf(member)

                this.members.splice(index, 1)
                this.$emit('update:members', this.members);
            },
            updateMembers(members) {
                this.$emit('update:members', members)

                this.$nextTick(() => {
                    this.search = null;
                });
            }
        },
        watch: {
            search(input) {
                if (!input || input.length < 3) {
                    return
                }

                if (this.pending) {
                    return;
                }

                this.pending = true;

                fetch(`http://localhost:8000/api/users/search?q=${input}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json'
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

                        const users = data.users;
                        outer: for (let i = 0; i < users.length; i++) {
                            for (let j = 0; j < this.entries.length; j++) {
                                if (users[i].id == this.entries[j].id) {
                                    continue outer;
                                }
                            }

                            this.entries.push(users[i]);
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.pending = false
                    });
            }
        }
    }
</script>