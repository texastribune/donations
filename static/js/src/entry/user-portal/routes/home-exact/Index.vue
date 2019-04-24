<template>
  <ul>
    <li v-for="datum in data" :key="datum.id">{{ datum.headline }}</li>
  </ul>
</template>

<script>
import axios from 'axios';

import routeMixin from '../../mixins/route';

export default {
  name: 'Index',

  mixins: [routeMixin],

  data() {
    return { data: [] };
  },

  methods: {
    async fetchData() {
      const {
        data: { results },
      } = await axios.get('https://www.texastribune.org/api/v2/content/');

      this.data = results;
    },
  },
};
</script>
