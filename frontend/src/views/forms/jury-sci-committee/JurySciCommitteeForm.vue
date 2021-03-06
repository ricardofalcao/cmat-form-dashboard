<template>
    <FormTemplate
            ref="form"
            id="jury-sci-committee"
            :form="submittableForm"
            @submit="submitEvent"
    >
        <template #form>
            <RawJurySciCommittee :form="form"></RawJurySciCommittee>
        </template>
    </FormTemplate>
</template>

<script>
    import FormTemplate from "@/components/forms/FormTemplate";
    import RawJurySciCommittee from "@/components/forms/RawJurySciCommittee";

    export default {
        name: 'JurySciCommitteeForm',
        components: {
            RawJurySciCommittee,
            FormTemplate
        },
        data() {
            const _defaultForm = {
                member: {},
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
                copy.member = copy.member.id

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
