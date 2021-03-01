<template>
    <FormTemplate
            id="event-organization"
            :form="submittableForm"
            @submit="submitEvent"
    >
        <template #form>
            <RawEventOrganization :form="form"></RawEventOrganization>
        </template>
    </FormTemplate>
</template>

<script>
    import FormTemplate from "@/components/forms/FormTemplate";
    import RawEventOrganization from "@/components/forms/RawEventOrganization";

    export default {
        name: 'EventOrganizationForm',
        components: {
            RawEventOrganization,
            FormTemplate
        },
        data() {
            const _defaultForm = {
                members: [],
                eventType: '',
                involvementType: '',
                regionType: '',
                designation: '',
                local: '',
                date: [],
                url: '',
                observations: '',
            }

            return {
                form: Object.assign( {}, _defaultForm),
                defaultForm: _defaultForm
            }
        },
        computed: {
            submittableForm() {
                const copy = Object.assign({}, this.form);
                copy.members = copy.members.map(m => m.id)

                return copy
            }
        },
        methods: {
            submitEvent() {
                this.form = Object.assign( {}, this.defaultForm);
                this.$refs.form.reset()
            }
        }
    }
</script>
