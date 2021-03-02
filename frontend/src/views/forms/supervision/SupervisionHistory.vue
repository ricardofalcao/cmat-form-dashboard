<template>
  <LogSupervision :userOnly="true" :showSchemas="false">

  </LogSupervision>
</template>

<script>
import LogSupervision from "@/components/logs/LogSupervision";

export default {
  name: 'SupervisionHistory',
  components: {
    LogSupervision
  },
  data() {
    return {

    }
  },
}
</script>
