<template>
    <div>
        <MembersInput
                :member.sync="form.member"
                :multiple="false"
                label="Member"
        />

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
                :items="['Editor', 'Referee', 'Reviewer']"
                v-model="form.type"

                :rules="[
                                        v => !!v || 'Type is required',
                                    ]"
                required

                label="Type"
        ></v-select>

        <v-select
                :items="['Journal', 'Proceedings', 'Other']"
                v-model="form.publicationType"

                :rules="[
                                        v => !!v || 'Publication type is required',
                                    ]"
                required

                label="Type"
        ></v-select>

        <v-text-field
                v-model="form.publication"
                :rules="[
                                        v => !!v || 'Publication name / Publisher is required',
                                    ]"
                required

                label="Publication name / Publisher"
        ></v-text-field>

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
        name: 'RawReferringEditorialAct',
        components: {
            MembersInput
        },
        props: {
            form: {
                type: Object
            }
        }
    }
</script>
