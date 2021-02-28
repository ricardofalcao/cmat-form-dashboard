<template>
  <FormTemplate
      id="event-participation"
      name="Participation in Events"
      :form="form"
  >
    <template #form>
      <v-select
          :items="['Conference', 'Seminar',  'Workshop', 'Short Course', 'Other']"
          v-model="form.eventType"

          :rules="[
                                        v => !!v || 'Event type is required',
                                    ]"
          required

          label="Type of Event"
      ></v-select>

      <v-select
          :items="['Invited Talk', 'Talk', 'Poster', 'No Communication']"
          v-model="form.participationType"

          :rules="[
                                        v => !!v || 'Participation type is required',
                                    ]"
          required

          label="Type of Participation"
      ></v-select>

      <v-text-field
          v-model="form.title"

          label="Title (if applicable)"
      ></v-text-field>

      <v-text-field
          v-model="form.event"
          :rules="[
                                        v => !!v || 'Event is required',
                                    ]"
          required

          label="Event"
      ></v-text-field>

      <v-text-field
          v-model="form.local"
          :rules="[
                                        v => !!v || 'Local is required',
                                    ]"
          required

          label="Local"
      ></v-text-field>

      <v-menu
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
              :value="formatDate"
              label="Date"
              readonly
              v-bind="attrs"
              v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
            v-model="form.date"
            range
        ></v-date-picker>
      </v-menu>

      <v-textarea
          v-model="form.observations"
          solo

          name="input-7-4"
          label="Observations"
      ></v-textarea>
    </template>
  </FormTemplate>
</template>

<script>
import FormTemplate from "@/components/FormTemplate";

export default {
  name: 'EventParticipation',
  components: {
    FormTemplate,
  },
  data() {
    return {
      form: {
        eventType: '',
        participationType: '',
        title: '',
        event: '',
        local: '',
        date: [new Date().toISOString().substr(0, 10), new Date().toISOString().substr(0, 10)],
        observations: '',
      }
    }
  },
  computed: {
    formatDate() {
      return this.form.date.join(' ~ ')
    }
  }
}
</script>
