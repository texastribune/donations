<template>
  <div
    :class="`grid_row grid_wrap--${wrapBreakPoint}`"
  >
    <card
      :options="options"
      class="donation--card col_8"
      stripe="pk_test_sSUhBbATSHteQVZZvz6R5aYe"
      @change="complete = $event.complete"
    />
    <div
      class="col_4"
    >
      <div
        class="grid_row"
      >
        <input
          :disabled="!complete"
          class="col button button--yellow button--l button--donate"
          type="submit"
          value="Donate"
          @click="pay"
        >
      </div>
    </div>
  </div>
</template>

<script>
import { Card, createToken } from 'vue-stripe-elements-plus';

export default {
  name: 'BasicPay',

  components: {
    Card,
  },

  props: {
    wrapBreakPoint: {
      type: String,
      default: 's',
    },
  },

  data() {
    return {
      complete: false,
      options: {
        hidePostalCode: true,
        iconStyle: 'solid',
      },
    };
  },

  methods: {
    pay() {
      createToken().then(({ token: { id } }) => {
        this.$emit('setToken', id);
      }).catch(() => {
        window.location.href = '/error';
      });
    },
  },
};
</script>
