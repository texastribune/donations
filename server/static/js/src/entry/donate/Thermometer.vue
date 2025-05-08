<template>
  <div v-if="!loading && !error" class="thermometer">
    <div class="bar" aria-hidden="true">
      <div class="bar_inner bar_inner--goal"></div>
      <div
        class="bar_inner bar_inner--actual"
        :style="{ width: `${actualWidth}%` }"
      ></div>
    </div>
    <div class="text">
      <strong>{{ data[0].label }} raised today</strong> <br />
      to unlock {{ data[1].label }} in matching funds.
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
        { slug: 'actual', label: '20', value: 20 },
        { slug: 'goal', label: '500', value: 500 },
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
      const url = 'https://membership.texastribune.org/fmd2024.json';

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
