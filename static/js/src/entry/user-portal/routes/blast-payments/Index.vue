<template>
  <p>This is Blast payments.</p>
</template>

<script>
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';

export default {
  name: 'Index',

  mixins: [routeMixin, routeFetchMixin],

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
