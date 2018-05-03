<template>
  <form
    action="/charge"
    method="post"
  >
    <radios
      :on-update="onFrequencyUpdate"
      :options="frequencyOptions"
      name="installment_period"
      store-module="baseForm"
    />
  </form>
</template>

<script>
// import HiddenInput from '../../elements/HiddenInput.vue';
import Radios from '../../elements/Radios.vue';
// import Level from '../../elements/Level.vue';
// import PayFees from '../../elements/PayFees.vue';
// import TextInput from '../../elements/TextInput.vue';

export default {
  name: 'TopForm',

  components: {
    // HiddenInput,
    // TextInput,
    Radios,
    // PayFees,
    // Level,
  },

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],
    };
  },

  methods: {
    onFrequencyUpdate(newVal) {
      let openEndedVal;

      if (newVal === 'yearly' || newVal === 'monthly') {
        openEndedVal = 'Open';
      } else if (newVal === 'None') {
        openEndedVal = 'None';
      }

      this.$store.dispatch(
        'baseForm/updateValue',
        { key: 'openended_status', value: openEndedVal },
      );
    },
  },
};
</script>
