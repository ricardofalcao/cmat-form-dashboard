<template>
    <LogTemplate
            id="supervision"
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

        <template v-slot:table.supervisors="{ item }">
            {{ getMembersNames(item.supervisors) }}
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
            <RawSupervision :form="item"></RawSupervision>
        </template>

    </LogTemplate>
</template>

<script>
    import LogTemplate from "@/components/logs/LogTemplate";
    import RawSupervision from "@/components/forms/RawSupervision";

    export default {
        name: 'LogSupervision',
        components: {
            RawSupervision,
            LogTemplate
        },
        data() {
            return {
                schemaVars: [
                    {title: 'User', description: 'user.name | user.email | user.group'},
                    {title: 'Student', description: 'student | studentCountry'},
                    {title: 'Supervisors', description: 'supervisors (User[])'},
                    {title: 'Type', description: 'type'},
                    {title: 'Situation', description: 'situation'},
                    {title: 'Title', description: 'title'},
                    {title: 'Institution', description: 'institution'},
                    {title: 'Course', description: 'course'},
                    {title: 'Date', description: 'dateStart | dateFinish'},
                    {title: 'Observations', description: 'observations'}
                ],

                headers: [
                    {text: 'User', value: 'user'},
                    {text: 'Student', value: 'student'},
                    {text: 'Student Country', value: 'studentCountry'},
                    {text: 'Supervisors', value: 'supervisors'},
                    {text: 'Type', value: 'type'},
                    {text: 'Situation', value: 'situation'},
                    {text: 'Title', value: 'title'},
                    {text: 'Institution', value: 'institution'},
                    {text: 'Course', value: 'course'},
                    {text: 'Date', value: 'dateStart'},
                    {text: 'Observations', value: 'observations', sortable: false}
                ],

                defaultItem: {
                    user: {},
                    student: '',
                    studentCountry: '',
                    supervisors: [],
                    type: '',
                    situation: '',
                    title: '',
                    institution: '',
                    course: '',
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
                copy.supervisors = copy.supervisors.map(m => m.id)

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
