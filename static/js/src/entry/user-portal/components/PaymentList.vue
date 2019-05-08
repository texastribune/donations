<template>
  <div>
    <table class="c-table c-table--bordered l-width-full">
      <thead>
        <tr>
          <th><strong>Date</strong></th>
          <th><strong>Amount</strong></th>
          <th><strong>Payment</strong></th>
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
    <button type="button" @click="$emit('onLoadMore')">Load more</button>
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
