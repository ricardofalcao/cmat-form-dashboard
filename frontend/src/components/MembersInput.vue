<template>
    <div class="members-input">
        <v-autocomplete
                :value="members"
                @input="updateMembers($event)"

                :rules="[
                                        v => !!v || 'Member list is required',
                                        v => v.length > 0 || 'At least one member must be specified',
                                    ]"
                required

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
        mounted() {
            let members = []

            for (let i = 0; i < this.members.length; i++) {
                members.push(this.members[i].name)
            }

            this.fetchMembers(members)
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
            },
            fetchMembers(members) {
                if (members.length == 0 || this.pending) {
                    return;
                }

                this.pending = true;

                let url = `http://localhost:8000/api/users/search?`
                for (let i = 0; i < members.length; i++) {
                    url += `q=${members[i]}&`
                }

                fetch(url, {
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
        },
        watch: {
            search(input) {
                if (!input || input.length < 3) {
                    return
                }

                this.fetchMembers([input])
            }
        }
    }
</script>