<template>
  <p>This is Blast payments.</p>
</template>

<script>
import routeMixin from '../../mixins/route';

export default {
  name: 'Index',

  mixins: [routeMixin],

  created() {
    // temp
    throw new Error();
  },

  methods: {
    async fetchData() {
      /* do nothing */
    },
  },
};
</script>
