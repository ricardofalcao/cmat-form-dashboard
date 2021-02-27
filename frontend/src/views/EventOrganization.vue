<template>
    <div class="event-organization pa-4">
        <v-card elevation="2">
            <v-card-text>
                <h4 class="text-h4 mb-4">Organization of Events</h4>


                <v-form
                        v-model="valid">

                    <MembersInput :members.sync="form.members" label="Members"/>

                    <v-radio-group
                            v-model="form.regionType"
                            row
                    >
                        <v-radio
                                label="National"
                                value="national"
                        ></v-radio>
                        <v-radio
                                label="International"
                                value="international"
                        ></v-radio>
                    </v-radio-group>

                    <v-select
                            :items="['Workshop', 'Scientific Meeting']"
                            v-model="form.type"

                            :rules="[
                                        v => !!v || 'Event type is required',
                                    ]"
                            required

                            label="Type of Event"
                    ></v-select>

                    <v-select
                            :items="['Organizer', 'Local Organizer', 'Other']"
                            v-model="form.involvement"

                            :rules="[
                                        v => !!v || 'Involvement type is required',
                                    ]"
                            required

                            label="Type of Involvement"
                    ></v-select>

                    <v-text-field
                            v-model="form.designation"
                            :rules="[
                                        v => !!v || 'Designation is required',
                                    ]"
                            required

                            label="Designation"
                    ></v-text-field>

                    <v-text-field
                            v-model="form.local"
                            :rules="[
                                        v => !!v || 'Local is required',
                                    ]"
                            required

                            label="Local"
                    ></v-text-field>

                    <v-menu
                            :close-on-content-click="false"
                            transition="scale-transition"
                            offset-y
                            min-width="auto"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
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

                    <v-text-field
                            v-model="form.url"
                            :rules="[
                                        v => !!v || 'URL is required',
                                    ]"
                            required

                            label="URL"
                    ></v-text-field>

                    <v-textarea
                            v-model="form.observations"
                            solo

                            name="input-7-4"
                            label="Observations"
                    ></v-textarea>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
    import MembersInput from "@/components/MembersInput";

    export default {
        name: 'EventOrganization',
        components: {
            MembersInput,
        },
        data() {
            return {
                valid: false,
                form: {
                    members: [],
                    type: '',
                    involvement: '',
                    regionType: '',
                    designation: '',
                    local: '',
                    date: [new Date().toISOString().substr(0, 10), new Date().toISOString().substr(0, 10)],
                    url: '',
                    observations: '',
                }
            }
        },
        computed: {
            formatDate() {
                return this.form.date.join(' ~ ')
            }
        }
    }
</script>
