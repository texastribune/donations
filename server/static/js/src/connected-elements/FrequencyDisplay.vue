<template>
  <div aria-live="polite" class="has-text-gray-dark">
    {{ installmentPeriod }}
  </div>
</template>

<script>
import updateValue from './mixins/update-value';
import getValue from './mixins/get-value';

export default {
  name: 'FrequencyDisplay',

  mixins: [updateValue, getValue],

  props: {
    storeModule: {
      type: String,
      required: true,
    },
  },

  computed: {
    installmentPeriod() {
      const installmentPeriod = this.getValue({
        storeModule: this.storeModule,
        key: 'installment_period',
      });

      if (installmentPeriod === 'None') return '';
      return `/${installmentPeriod.toLowerCase()}`;
    },
  },


};
</script>
