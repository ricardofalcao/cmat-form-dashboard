<template>
  <LogJurySciCommittee :userOnly="true" :showSchemas="false">

  </LogJurySciCommittee>
</template>

<script>
import LogJurySciCommittee from "@/components/logs/LogJurySciCommittee";

export default {
  name: 'JurySciCommitteeHistory',
  components: {
    LogJurySciCommittee
  },
  data() {
    return {

    }
  },
}
</script>
