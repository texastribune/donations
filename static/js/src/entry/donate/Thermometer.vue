<template>
  <div class="thermometer">
    <div class="bar">
      <div class="bar_inner bar_inner--goal"></div>
      <div class="bar_inner bar_inner--actual" :style="{width: `${actualWidth}%`}"></div>
    </div>
    <div class="text">
      <strong>{{ data[0].label }} new members</strong>
      <br>
      toward goal of {{ data[1].label }}.
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
        { slug: 'goal', label: '350', value: 350 },
      ],
    };
  },
  computed: {
    actualWidth: function() {
      return ((this.data[0].value / this.data[1].value) * 100);
    }
  },
  mounted() {
    this.getSalesforceReport();
  },
  methods: {
    getSalesforceReport() {
      // const url = 'https://membership.texastribune.org/smd18-report.json';
      const url = 'https://membership.texastribune.org/fmd18-members.json';
      axios.get(url)
        .then(({
          data: {
            // 'factMap': { 'T!T': { 'aggregates': [actual, goal] } },
            'value': actual_value,
            'label': actual_label,
          },
        }) => {
          // this.data[0].label = actual.label;
          // this.data[0].value = actual.value;
          // this.data[1].label = goal.label;
          // this.data[1].value = goal.value;
          this.data[0].label = actual_label;
          this.data[0].value = actual_value;
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
