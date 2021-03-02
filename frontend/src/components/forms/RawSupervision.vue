<template>
    <div>
        <v-text-field
                v-model="form.student"
                :rules="[
                                        v => !!v || 'Student name is required',
                                    ]"
                required

                label="Student name"
        ></v-text-field>

        <v-select
                :items="countryList"
                v-model="form.studentCountry"

                :rules="[
                                        v => !!v || 'Student country is required',
                                    ]"
                required

                label="Student country"
        ></v-select>

        <MembersInput
                :members.sync="form.supervisors"
                label="Supervisors"
        />

        <v-select
                :items="['Msc', 'PhD', 'Post-doc', 'Other']"
                v-model="form.type"

                :rules="[
                                        v => !!v || 'Type is required',
                                    ]"
                required

                label="Type"
        ></v-select>

        <v-select
                :items="['Completed', 'Give up', 'In course']"
                v-model="form.situation"

                :rules="[
                                        v => !!v || 'Situation is required',
                                    ]"
                required

                label="Situation"
        ></v-select>

        <v-text-field
                v-model="form.title"
                :rules="[
                                        v => !!v || 'Title is required',
                                    ]"
                required

                label="Title"
        ></v-text-field>

        <v-text-field
                v-model="form.institution"
                :rules="[
                                        v => !!v || 'Institution is required',
                                    ]"
                required

                label="Institution"
        ></v-text-field>

        <v-text-field
                v-model="form.course"
                :rules="[
                                        v => !!v || 'Course is required',
                                    ]"
                required

                label="Course"
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
    import { countryList } from "@/utils/constants"

    export default {
        name: 'RawSupervision',
        components: {
            MembersInput
        },
        props: {
            form: {
                type: Object
            }
        },
        data() {
            return {
                countryList: countryList
            }
        },
        computed: {
            formatDate() {
                return this.form.date.join(' ~ ')
            }
        }
    }
</script>
