<template>
    <FormTemplate
            id="event-participation"
            :form="form"
            @submit="submitEvent"
    >
        <template #form>
            <RawEventParticipation :form="form"></RawEventParticipation>
        </template>
    </FormTemplate>
</template>

<script>
    import FormTemplate from "@/components/forms/FormTemplate";
    import RawEventParticipation from "@/components/forms/RawEventParticipation";

    export default {
        name: 'EventParticipationForm',
        components: {
            FormTemplate,
            RawEventParticipation
        },
        data() {
            const _defaultForm = {
                eventType: '',
                participationType: '',
                title: '',
                event: '',
                local: '',
                date: [],
                observations: '',
            };

            return {
                snackbar: false,
                form: Object.assign({}, _defaultForm),
                defaultForm: _defaultForm
            }
        },
        computed: {
            formatDate() {
                return this.form.date.join(' ~ ')
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
