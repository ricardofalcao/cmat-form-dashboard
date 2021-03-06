<template>
  <LogTemplate
      id="referring-editorial-act"
      v-bind="$attrs"
      :headers="headers"
      :default-item="defaultItem"
      :preprocess-outbound="preprocessForm"
      :preprocess-inbound="preprocessItem"
      :date-search="true"
      :schema-vars="schemaVars"
  >

    <template v-slot:table.user="{ item }">
      {{ item.user.name }}
    </template>

    <template v-slot:table.member="{ item }">
      {{ item.member.name }}
    </template>

    <template v-slot:table.observations="{ item }">
      {{
        item.observations ? item.observations.length > 20 ? `${item.observations.substring(0, 17)}...` :
            item.observations : 'none'
      }}
    </template>

    <template #dialog="{ item }">
      <RawReferringEditorialAct :form="item"></RawReferringEditorialAct>
    </template>

  </LogTemplate>
</template>

<script>
import LogTemplate from "@/components/logs/LogTemplate";
import RawReferringEditorialAct from "@/components/forms/RawReferringEditorialAct";

export default {
  name: 'LogJurySciCommittee',
  components: {
    RawReferringEditorialAct,
    LogTemplate
  },
  data() {
    return {
      schemaVars: [
        {title: 'User', description: 'user.name | user.shortName | user.authorName | user.email | user.group'},
        {title: 'Member', description: 'member (User)'},
        {title: 'Region', description: 'regionType'},
        {title: 'Type', description: 'type'},
        {title: 'Type of Publication', description: 'publicationType'},
        {title: 'Publication', description: 'publication'},
        {title: 'Reviews', description: 'reviews'},
        {title: 'Year', description: 'year'},
        {title: 'Observations', description: 'observations'}
      ],

      headers: [
        {text: 'User', value: 'user'},
        {text: 'Member', value: 'member', sortable: false},
        {text: 'Region', value: 'regionType'},
        {text: 'Type', value: 'type'},
        {text: 'Type of Publication', value: 'publicationType'},
        {text: 'Publication', value: 'publication', sortable: false},
        {text: 'Reviews', value: 'reviews'},
        {text: 'Year', value: 'year'},
        {text: 'Observations', value: 'observations', sortable: false}
      ],

      defaultItem: {
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
    }
  },
  methods: {
    preprocessForm(form) {
      const copy = Object.assign({}, form);
      copy.member = copy.member.id

      return copy
    },
    preprocessItem(item) {
      item.year = item.year.toString()
      return item
    }
  }
}
</script>
