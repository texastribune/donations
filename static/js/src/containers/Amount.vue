<template>
  <input
    :value="amount"
    type="text"
    @input="updateAmount($event.target.value)"
  >
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Amount',

  props: {
    useQueryParam: {
      type: Boolean,
      default: true,
    },

    useStore: {
      type: Boolean,
      default: true,
    },

    paramAmount: {
      type: String,
      default: '',
    },
  },

  data() {
    if (this.useQueryParam) {
      return {
        localAmount: this.paramAmount,
      };
    }
    return {};
  },

  computed: {
    ...mapGetters('form', [
      'storeValue',
    ]),

    amount() {
      if (this.useStore) {
        return this.storeValue('amount');
      }
      return this.localAmount;
    },
  },

  watch: {
    paramAmount(newAmount, oldAmount) {
      const shouldUpdate =
        (oldAmount !== newAmount) &&
        this.useQueryParam;

      if (shouldUpdate) {
        this.updateAmount(newAmount);
      }
    },
  },

  methods: {
    ...mapActions('form', ['updateStoreValue']),

    updateAmount(newAmount) {
      if (this.useStore) {
        this.updateStoreValue({
          key: 'amount',
          value: newAmount,
        });
      } else {
        this.localAmount = newAmount;
      }
    },
  },
};
</script>
