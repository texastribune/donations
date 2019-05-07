<template>
  <p>This is Blast.</p>
</template>

<script>
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';

export default {
  name: 'Index',

  mixins: [routeMixin, routeFetchMixin],

  methods: {
    async fetchData() {
      /* do nothing */
    },
  },
};
</script>
