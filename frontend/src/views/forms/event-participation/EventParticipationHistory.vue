<template>
  <LogEventParticipation :userOnly="true" :showSchemas="false">

  </LogEventParticipation>
</template>

<script>
import LogEventParticipation from "@/components/logs/LogEventParticipation";

export default {
  name: 'EventParticipationHistory',
  components: {
    LogEventParticipation
  },
  data() {
    return {

    }
  },
}
</script>
