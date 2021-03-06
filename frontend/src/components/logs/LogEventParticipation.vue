<template>
    <LogTemplate
            id="event-participation"
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

        <template v-slot:table.group="{ item }">
            {{ item.user.group }}
        </template>

        <template v-slot:table.title="{ item }">
            {{ item.title ? item.title : 'none' }}
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
            <RawEventParticipation :form="item"></RawEventParticipation>
        </template>
    </LogTemplate>
</template>

<script>
    import LogTemplate from "@/components/logs/LogTemplate";
    import RawEventParticipation from "@/components/forms/RawEventParticipation";

    export default {
        name: 'LogEventParticipation',
        components: {
            RawEventParticipation,
            LogTemplate
        },
        data() {
            return {
                schemaVars: [
                    {title: 'User', description: 'user.name | user.shortName | user.authorName | user.email | user.group'},
                    {title: 'Group', description: 'group'},
                    {title: 'Type of Event', description: 'eventType'},
                    {title: 'Type of Participation', description: 'participationType'},
                    {title: 'Title', description: 'title'},
                    {title: 'Event', description: 'event'},
                    {title: 'Local', description: 'local'},
                    {title: 'Date', description: 'dateStart | dateFinish'},
                    {title: 'Observations', description: 'observations'}
                ],

                headers: [
                    {text: 'User', value: 'user'},
                    {text: 'Group', value: 'group'},
                    {text: 'Type of Event', value: 'eventType'},
                    {text: 'Type of Participation', value: 'participationType'},
                    {text: 'Title', value: 'title'},
                    {text: 'Event', value: 'event'},
                    {text: 'Local', value: 'local'},
                    {text: 'Date', value: 'dateStart'},
                    {text: 'Observations', value: 'observations', sortable: false}
                ],

                defaultItem: {
                    user: {},
                    eventType: '',
                    participationType: '',
                    title: '',
                    event: '',
                    local: '',
                    date: [],
                    dateStart: null,
                    dateFinish: null,
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
