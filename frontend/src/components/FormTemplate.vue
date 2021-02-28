<template>
  <div :class="`log-${id}`" class="pa-4">
    <v-card elevation="2">
      <v-card-title class="mt-4 text-center justify-center py-2">
        <h4 class="text-h4">{{ name }}</h4>
      </v-card-title>

      <v-tabs
          class="mt-4"
          grow
      >
        <v-tab>Form</v-tab>
        <v-tab>History</v-tab>
      </v-tabs>
      <v-card-text class="mt-4">

        <v-form
            v-model="valid">

          <slot name="form"></slot>

          <v-btn
              :disabled="pending"
              type="submit"
              color="success"
              outlined

              @click.prevent="submitForm"
          >
            Submit
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'LogTemplate',
  props: {
    id: {
      type: String
    },
    name: {
      type: String
    },
    form: {
      type: Object
    }
  },
  data() {
    return {
      valid: false,
      pending: false
    }
  },
  methods: {
    submitForm() {
      if (!this.valid) {
        return;
      }

      this.pending = true;

      fetch(`http://localhost:8000/api/forms/${this.id}`, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.form)
      })
          .then(async response => {
            const data = await response.json();

            // check for error response
            if (!response.ok) {
              // get error message from body or default to response status
              const error = (data && data.detail) || response.status;
              return Promise.reject(error);
            }

            console.log(data)
          })
          .catch(error => {
            console.log(error);
          })
          .finally(() => {
            this.pending = false
          });
    }
  }
}
</script>
