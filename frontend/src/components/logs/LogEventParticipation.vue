<template>
  <LogTemplate
      id="event-participation"
      v-bind="$attrs"
      :headers="headers"
      :default-item="defaultItem"
  >

    <template v-slot:table.user="{ item }">
      {{ item.user.name }}
    </template>

    <template v-slot:table.title="{ item }">
      {{ item.title ? item.title : 'none' }}
    </template>

    <template v-slot:table.date="{ item }">
      {{ `${item.dateStart}~${item.dateFinish}` }}
    </template>

    <template v-slot:table.observations="{ item }">
      {{
        item.observations ? item.observations.length > 20 ? `${item.observations.substring(0, 17)}...` :
            item.observations : 'none'
      }}
    </template>

    <template #dialog="{ item }">
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>User</v-list-item-title>
            <v-list-item-subtitle>{{ item.user.name }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Type of Event</v-list-item-title>
            <v-list-item-subtitle>{{ item.eventType }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Type of Participation</v-list-item-title>
            <v-list-item-subtitle>{{ item.participationType }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item v-if="item.title">
          <v-list-item-content>
            <v-list-item-title>Title</v-list-item-title>
            <v-list-item-subtitle>{{ item.title }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Event</v-list-item-title>
            <v-list-item-subtitle>{{ item.event }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Local</v-list-item-title>
            <v-list-item-subtitle>{{ item.local }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Date</v-list-item-title>
            <v-list-item-subtitle>{{
                `${item.dateStart}~${item.dateFinish}`
              }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item v-if="item.observations" three-line>
          <v-list-item-content>
            <v-list-item-title>Observations</v-list-item-title>
            <v-list-item-subtitle>{{ item.observations }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>

  </LogTemplate>
</template>

<script>
import LogTemplate from "@/components/logs/LogTemplate";

export default {
  name: 'LogEventParticipation',
  components: {
    LogTemplate
  },
  data() {
    return {
      headers: [
        {text: 'User', value: 'user'},
        {text: 'Type of Event', value: 'eventType'},
        {text: 'Type of Participation', value: 'participationType'},
        {text: 'Title', value: 'title'},
        {text: 'Event', value: 'event'},
        {text: 'Local', value: 'local'},
        {text: 'Date', value: 'date'},
        {text: 'Observations', value: 'observations'}
      ],

      defaultItem: {
        user: {},
        eventType: '',
        participationType: '',
        title: '',
        event: '',
        local: '',
        dateStart: null,
        dateFinish: null,
        observations: '',
      }
    }
  }
}
</script>
