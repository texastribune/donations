<template>
  <p
    v-if="level"
    :class="getCssClasses('para')"
  >
    Your giving level is:
    <span
      :class="getCssClasses('span')"
    >
      {{ level }}
    </span>
  </p>
</template>

<script>
export default {
  name: 'Level',

  props: {
    amountStoreModule: {
      type: String,
      required: true,
    },

    installmentPeriodStoreModule: {
      type: String,
      required: true,
    },

    paraCssClasses: {
      type: [String, Array],
      default: '',
    },

    spanCssClasses: {
      type: [String, Array],
      default: '',
    },
  },

  computed: {
    level() {
      const amountGetter =
        this.$store.getters[`${this.amountStoreModule}/valueByKey`];
      const installmentPeriodGetter =
        this.$store.getters[`${this.installmentPeriodStoreModule}/valueByKey`];

      const amount = parseFloat(amountGetter('amount'));
      const installmentPeriod = installmentPeriodGetter('installment_period');

      if (Number.isNaN(amount) || !amount) return '';

      if (installmentPeriod === 'monthly') {
        if (amount >= 3 && amount <= 8) {
          return 'Informed';
        } else if (amount >= 9 && amount <= 41) {
          return 'Engaged';
        } else if (amount >= 42 && amount <= 83) {
          return 'Involved';
        } else if (amount >= 84 && amount <= 208) {
          return 'Editor\'s Circle';
        } else if (amount >= 209 && amount <= 416) {
          return 'Leadership Circle';
        } else if (amount >= 417) {
          return 'Chairman\'s Circle';
        }
        return '';
      } else if (installmentPeriod === 'yearly') {
        if (amount === 10) {
          return 'Student';
        } else if (amount >= 35 && amount <= 99) {
          return 'Informed';
        } else if (amount >= 100 && amount <= 499) {
          return 'Engaged';
        } else if (amount >= 500 && amount <= 999) {
          return 'Involved';
        } else if (amount >= 1000 && amount <= 2499) {
          return 'Editor\'s Circle';
        } else if (amount >= 2500 && amount <= 4999) {
          return 'Leadership Circle';
        } else if (amount >= 5000) {
          return 'Chairman\'s Circle';
        }
        return '';
      }

      return '';
    },
  },
};
</script>
