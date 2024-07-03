<template>
  <p v-if="!loading && !error">
    <strong>We've raised {{ data[0].label }} </strong> toward a goal of {{ data[1].label }}
  </p>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Thermometer',

  data() {
    return {
      loading: true,
      error: false,
      data: [
        { slug: 'actual', label: '0', value: 0 },
        { slug: 'goal', label: '$20,000', value: 20000 },
      ],
    };
  },

  computed: {
    actualWidth() {
      return (this.data[0].value / this.data[1].value) * 100;
    },
  },

  mounted() {
    this.getSalesforceReport();
  },

  methods: {
    getSalesforceReport() {
      const url = 'https://membership.texastribune.org/border2024.json';

      axios
        .get(url)
        .then(({ data: { value: actualValue, label: actualLabel } }) => {
          this.data[0].label = actualLabel;
          this.data[0].value = actualValue;
          this.loading = false;
        })
        .catch(() => {
          this.error = true;
          this.loading = false;
        });
    },
  },
};
</script>
