<template>
    <FormTemplate
            id="event-organization"
            :form="submittableForm"
    >
        <template #form>
            <MembersInput :members.sync="form.members" label="Members"/>

            <v-radio-group
                    v-model="form.regionType"

                    :rules="[
                                        v => !!v || 'Region type is required',
                                    ]"

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
                    v-model="form.eventType"

                    :rules="[
                                        v => !!v || 'Event type is required',
                                    ]"
                    required

                    label="Type of Event"
            ></v-select>

            <v-select
                    :items="['Organizer', 'Local Organizer', 'Other']"
                    v-model="form.involvementType"

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
        </template>
    </FormTemplate>
</template>

<script>
    import MembersInput from "@/components/MembersInput";
    import FormTemplate from "@/components/forms/FormTemplate";

    export default {
        name: 'EventOrganizationForm',
        components: {
            MembersInput,
            FormTemplate
        },
        data() {
            return {
                form: {
                    members: [],
                    eventType: '',
                    involvementType: '',
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
            },
            submittableForm() {
                const copy = Object.assign({}, this.form);
                copy.members = copy.members.map(m => m.id)

                return copy
            }
        }
    }
</script>
