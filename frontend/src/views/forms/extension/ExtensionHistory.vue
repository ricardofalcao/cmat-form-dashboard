<template>
  <LogExtension :userOnly="true" :showSchemas="false">

  </LogExtension>
</template>

<script>
import LogExtension from "@/components/logs/LogExtension";

export default {
  name: 'ExtensionHistory',
  components: {
    LogExtension
  },
  data() {
    return {

    }
  },
}
</script>
