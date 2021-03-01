<template>
    <LogTemplate
            id="event-participation"
            v-bind="$attrs"
            :headers="headers"
            :default-item="defaultItem"
            :preprocess-outbound="preprocessForm"
            :preprocess-inbound="preprocessItem"
            :date-search="true"
            :show-schemas="true"
    >

        <template v-slot:table.user="{ item }">
            {{ item.user.name }}
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
                headers: [
                    {text: 'User', value: 'user'},
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
