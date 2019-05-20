<template>
  <div class="c-payments has-more l-width-full">
    <table class="c-table c-table--bordered l-width-full">
      <thead>
        <tr>
          <th class="t-align-left"><strong>Date</strong></th>
          <th class="t-align-left"><strong>Amount</strong></th>
          <th class="t-align-left"><strong>Payment</strong></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payment in payments" :key="payment.id">
          <td>
            <slot name="date" :date="payment.date"> {{ payment.date }} </slot>
          </td>
          <td>
            <slot name="amount" :date="payment.amount">
              {{ payment.amount }}
            </slot>
          </td>
          <td>
            <slot name="method" :date="payment.method">
              {{ payment.method }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
    <button
      class="c-button c-button--s has-bg-white has-box-shadow"
      type="button"
      @click="$emit('onLoadMore')"
    >
      Load more
    </button>
  </div>
</template>

<script>
export default {
  name: 'PaymentList',

  props: {
    payments: {
      type: Array,
      required: true,
    },
  },
};
</script>
