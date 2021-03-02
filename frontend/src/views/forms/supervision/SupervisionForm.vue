<template>
    <FormTemplate
            id="supervision"
            :form="submittableForm"
            @submit="submitEvent"
    >
        <template #form>
            <RawSupervision :form="form"></RawSupervision>
        </template>
    </FormTemplate>
</template>

<script>
    import FormTemplate from "@/components/forms/FormTemplate";
    import RawSupervision from "@/components/forms/RawSupervision";

    export default {
        name: 'SupervisionForm',
        components: {
            RawSupervision,
            FormTemplate
        },
        data() {
            const _defaultForm = {
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

            return {
                form: Object.assign({}, _defaultForm),
                defaultForm: _defaultForm
            }
        },
        computed: {
            submittableForm() {
                const copy = Object.assign({}, this.form);
                copy.supervisors = copy.supervisors.map(m => m.id)

                return copy
            }
        },
        methods: {
            submitEvent() {
                this.form = Object.assign({}, this.defaultForm);
                this.$refs.form.reset()
            }
        }
    }
</script>
