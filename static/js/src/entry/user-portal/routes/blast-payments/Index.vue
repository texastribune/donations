<template>
  <p>This is Blast payments.</p>
</template>

<script>
import routeMixin from '../../mixins/route';

export default {
  name: 'Index',

  mixins: [routeMixin],

  methods: {
    async fetchData() {
      /* do nothing */
    },
  },
};
</script>
