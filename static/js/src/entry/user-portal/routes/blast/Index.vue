<template>
  <p>This is Blast.</p>
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
