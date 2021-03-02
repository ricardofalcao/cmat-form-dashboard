<template>
  <LogEventOrganization :userOnly="true" :showSchemas="false">

  </LogEventOrganization>
</template>

<script>
import LogEventOrganization from "@/components/logs/LogEventOrganization";

export default {
  name: 'EventOrganizationHistory',
  components: {
    LogEventOrganization
  },
  data() {
    return {

    }
  },
}
</script>
