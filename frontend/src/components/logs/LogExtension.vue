<template>
    <LogTemplate
            id="extension"
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
            <RawExtension :form="item"></RawExtension>
        </template>

    </LogTemplate>
</template>

<script>
    import LogTemplate from "@/components/logs/LogTemplate";
    import RawExtension from "@/components/forms/RawExtension";

    export default {
        name: 'LogExtension',
        components: {
            RawExtension,
            LogTemplate
        },
        data() {
            return {
                schemaVars: [
                    {title: 'User', description: 'user.name | user.email | user.group'},
                    {title: 'Members', description: 'members (User[])'},
                    {title: 'Type', description: 'type'},
                    {title: 'Description', description: 'description'},
                    {title: 'Date', description: 'dateStart | dateFinish'},
                    {title: 'Observations', description: 'observations'}
                ],

                headers: [
                    {text: 'User', value: 'user'},
                    {text: 'Members', value: 'members'},
                    {text: 'Type', value: 'type'},
                    {text: 'Description', value: 'description'},
                    {text: 'Date', value: 'dateStart'},
                    {text: 'Observations', value: 'observations', sortable: false}
                ],

                defaultItem: {
                    user: {},
                    members: [],
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
