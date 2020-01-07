<template>
  <info-list :items="data" />
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'BlastDetail',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },
  },
};
</script>
