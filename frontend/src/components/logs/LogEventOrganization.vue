<template>
    <LogTemplate
            id="event-organization"
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

        <template v-slot:table.members="{ item }">
            {{ getMembersNames(item.members) }}
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
            <RawEventOrganization :form="item"></RawEventOrganization>
        </template>

    </LogTemplate>
</template>

<script>
    import LogTemplate from "@/components/logs/LogTemplate";
    import RawEventOrganization from "@/components/forms/RawEventOrganization";

    export default {
        name: 'LogEventOrganization',
        components: {
            RawEventOrganization,
            LogTemplate
        },
        data() {
            return {
                schemaVars: [
                    {title: 'User', description: 'user.name | user.shortName | user.authorName | user.email | user.group'},
                    {title: 'Members', description: 'members (User[])'},
                    {title: 'Type of Event', description: 'eventType'},
                    {title: 'Type of Participation', description: 'participationType'},
                    {title: 'Designation', description: 'designation'},
                    {title: 'Local', description: 'local'},
                    {title: 'Date', description: 'dateStart | dateFinish'},
                    {title: 'URL', description: 'url'},
                    {title: 'Observations', description: 'observations'}
                ],

                headers: [
                    {text: 'User', value: 'user'},
                    {text: 'Members', value: 'members'},
                    {text: 'Type of Event', value: 'eventType'},
                    {text: 'Type of Involvement', value: 'involvementType'},
                    {text: 'Designation', value: 'designation'},
                    {text: 'Local', value: 'local'},
                    {text: 'Date', value: 'dateStart'},
                    {text: 'URL', value: 'url', sortable: false},
                    {text: 'Observations', value: 'observations', sortable: false}
                ],

                defaultItem: {
                    user: {},
                    members: [],
                    eventType: '',
                    involvementType: '',
                    designation: '',
                    local: '',
                    date: [],
                    url: '',
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
            getMembersNames(members) {
                const membersNames = members.map(m => m.name).join(', ');
                return membersNames.length > 20 ? `${membersNames.substring(0, 17)}...` : membersNames;
            },
            preprocessForm(form) {
                const copy = Object.assign({}, form);
                copy.members = copy.members.map(m => m.id)

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
