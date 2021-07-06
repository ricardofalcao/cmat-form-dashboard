<template>
    <div>
        <MembersInput
                :members.sync="form.members"
                label="Members"
        />

        <v-select
                :items="['Divulgation', 'Transfer of Technology']"
                v-model="form.type"

                :rules="[
                                        v => !!v || 'Type is required',
                                    ]"
                required

                label="Type"
        ></v-select>

        <v-text-field
                v-model="form.description"
                :rules="[
                                        v => !!v || 'Description is required',
                                    ]"
                required

                label="Description"
        ></v-text-field>

        <v-menu
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-text-field
                        :rules="[
                            v => form.date.length == 2 ? true : form.date.length == 1 ? 'Finish date is required' : 'Start and finish date are required',
                        ]"
                        :value="formatDate"
                        label="Date"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                ></v-text-field>
            </template>
            <v-date-picker
                    v-model="form.date"
                    range
            ></v-date-picker>
        </v-menu>

        <v-textarea
                v-model="form.observations"
                solo

                name="input-7-4"
                label="Observations"
        ></v-textarea>
    </div>
</template>

<script>
    import MembersInput from "@/components/MembersInput";

    export default {
        name: 'RawExtension',
        components: {
            MembersInput
        },
        props: {
            form: {
                type: Object
            }
        },
        computed: {
            formatDate() {
                return this.form.date.join(' ~ ')
            }
        }
    }
</script>
