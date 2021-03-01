<template>
  <LogTemplate
      id="event-organization"
      v-bind="$attrs"
      :headers="headers"
      :default-item="defaultItem"
  >

    <template v-slot:table.user="{ item }">
      {{ item.user.name }}
    </template>

    <template v-slot:table.members="{ item }">
      {{ getMembersNames(item.members) }}
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
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>User</v-list-item-title>
            <v-list-item-subtitle>{{ item.user.name }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Members</v-list-item-title>
            <v-list-item-subtitle>{{ item.members.map(m => m.name).join(', ') }}</v-list-item-subtitle>
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
            <v-list-item-title>Type of Involvement</v-list-item-title>
            <v-list-item-subtitle>{{ item.involvementType }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Designation</v-list-item-title>
            <v-list-item-subtitle>{{ item.designation }}</v-list-item-subtitle>
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

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>URL</v-list-item-title>
            <v-list-item-subtitle>{{ item.url }}</v-list-item-subtitle>
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
  name: 'LogEventOrganization',
  components: {
    LogTemplate
  },
  data() {
    return {
      headers: [
        {text: 'User', value: 'user'},
        {text: 'Members', value: 'members'},
        {text: 'Type of Event', value: 'eventType'},
        {text: 'Type of Involvement', value: 'involvementType'},
        {text: 'Designation', value: 'designation'},
        {text: 'Local', value: 'local'},
        {text: 'Date', value: 'dateStart'},
        {text: 'URL', value: 'url', sortable: false},
        {text: 'Observations', value: 'observations', sortable: false}
      ],

      defaultItem: {
        user: {},
        members: [],
        eventType: '',
        involvementType: '',
        designation: '',
        local: '',
        dateStart: null,
        dateFinish: null,
        url: '',
        observations: '',
      }
    }
  },
  methods: {
    getMembersNames(members) {
      const membersNames = members.map(m => m.name).join(', ');
      return membersNames.length > 20 ? `${membersNames.substring(0, 17)}...` : membersNames;
    }
  }
}
</script>
