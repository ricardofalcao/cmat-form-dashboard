<template>
    <FormTemplate
            id="extension"
            :form="submittableForm"
            @submit="submitEvent"
    >
        <template #form>
            <RawExtension :form="form"></RawExtension>
        </template>
    </FormTemplate>
</template>

<script>
    import FormTemplate from "@/components/forms/FormTemplate";
    import RawExtension from "@/components/forms/RawExtension";

    export default {
        name: 'ExtensionForm',
        components: {
            RawExtension,
            FormTemplate
        },
        data() {
            const _defaultForm = {
                members: [],
                type: '',
                description: '',
                date: [],
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
