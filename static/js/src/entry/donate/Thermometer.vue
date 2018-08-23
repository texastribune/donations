<template>
  <div class="thermometer">
    <div class="bar">
      <div class="bar_inner bar_inner--goal"></div>
      <div class="bar_inner bar_inner--actual"></div>
    </div>
    <div class="text">
      <strong>{{ data[0].label }} new members</strong> towards goal of {{ data[1].label }}.
    </div>
  </div>
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
        { slug: 'goal', label: '0', value: 0 },
      ],
    };
  },
  mounted() {
    this.getSalesforceReport();
  },
  methods: {
    getSalesforceReport() {
      const url = 'https://membership.texastribune.org/smd18-report.json';
      axios.get(url)
        .then(({
          data: {
            'factMap': { 'T!T': { 'aggregates': [actual, goal] } },
          },
        }) => {
          this.data[0].label = actual.label;
          this.data[0].value = actual.value;
          this.data[1].label = goal.label;
          this.data[1].value = goal.value;
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
