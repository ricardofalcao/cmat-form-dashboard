<template>
    <LogTemplate
            id="jury-sci-committee"
            v-bind="$attrs"
            :headers="headers"
            :default-item="defaultItem"
            :preprocess-outbound="preprocessForm"
            :preprocess-inbound="preprocessItem"
            :date-search="true"
            :schema-vars="schemaVars"
    >

        <template v-slot:table.user="{ item }">
            {{ item.user.name }}
        </template>

        <template v-slot:table.member="{ item }">
            {{ item.member.name }}
        </template>

        <template v-slot:table.dateStart="{ item }">
            {{ `${item.dateStart}~${item.dateFinish}` }}
        </template>

        <template v-slot:table.observations="{ item }">
            {{
            item.observations ? item.observations.length > 20 ? `${item.observations.substring(0, 17)}...` :
            item.observations : 'none'
            }}
        </template>

        <template #dialog="{ item }">
            <RawJurySciCommittee :form="item"></RawJurySciCommittee>
        </template>

    </LogTemplate>
</template>

<script>
    import LogTemplate from "@/components/logs/LogTemplate";
    import RawJurySciCommittee from "../forms/RawJurySciCommittee";

    export default {
        name: 'LogJurySciCommittee',
        components: {
            RawJurySciCommittee,
            LogTemplate
        },
        data() {
            return {
                schemaVars: [
                    {title: 'User', description: 'user.name | user.email | user.group'},
                    {title: 'Member', description: 'member (User)'},
                    {title: 'Type', description: 'type'},
                    {title: 'Description', description: 'description'},
                    {title: 'Date', description: 'dateStart | dateFinish'},
                    {title: 'Observations', description: 'observations'}
                ],

                headers: [
                    {text: 'User', value: 'user'},
                    {text: 'Member', value: 'member', sortable: false},
                    {text: 'Type', value: 'type'},
                    {text: 'Description', value: 'description', sortable: false},
                    {text: 'Date', value: 'dateStart'},
                    {text: 'Observations', value: 'observations', sortable: false}
                ],

                defaultItem: {
                    user: {},
                    member: {},
                    type: '',
                    description: '',
                    date: [],
                    observations: '',
                }
            }
        },
        computed: {
            formatDate() {
                return this.form.date.join(' ~ ')
            }
        },
        methods: {
            preprocessForm(form) {
                const copy = Object.assign({}, form);
                copy.member = copy.member.id

                delete copy.dateStart
                delete copy.dateFinish

                return copy
            },
            preprocessItem(item) {
                item.date = [item.dateStart, item.dateFinish]

                return item
            }
        }
    }
</script>
