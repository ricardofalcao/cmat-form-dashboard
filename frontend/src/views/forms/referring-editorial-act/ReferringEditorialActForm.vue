<template>
  <FormTemplate
      ref="form"
      id="referring-editorial-act"
      :form="submittableForm"
      @submit="submitEvent"
  >
    <template #form>
      <RawReferringEditorialAct :form="form"></RawReferringEditorialAct>
    </template>
  </FormTemplate>
</template>

<script>
import FormTemplate from "@/components/forms/FormTemplate";
import RawReferringEditorialAct from "@/components/forms/RawReferringEditorialAct";

export default {
  name: 'ReferringEditorialActForm',
  components: {
    RawReferringEditorialAct,
    FormTemplate
  },
  data() {
    const _defaultForm = {
      user: {},
      member: {},
      type: '',
      regionType: '',
      publicationType: '',
      publication: '',
      reviews: 0,
      year: 0,
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
      copy.member = copy.member.id

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
