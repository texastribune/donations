<template>
  <div
    class="c-payments l-width-full"
    :class="{ 'has-more': offset < payments.length }"
  >
    <table class="c-table c-table--bordered l-width-full">
      <thead>
        <tr>
          <th class="t-align-left"><strong>Date</strong></th>
          <th class="t-align-left"><strong>Amount</strong></th>
          <th class="t-align-left"><strong>Payment</strong></th>
          <th v-if="showReceipts" class="t-align-left is-hidden-until-bp-l">
            <strong>Receipt</strong>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payment in slicedPayments" :key="payment.id">
          <td>
            <slot name="date" :date="payment.date">
              {{ payment.date | shortDate }}
            </slot>
          </td>
          <td>
            <slot name="amount" :amount="payment.amount">
              {{ payment.amount | currency }}
            </slot>
          </td>
          <td>
            <slot name="method" :method="payment.method">
              {{ payment.method }}
            </slot>
          </td>
          <td v-if="showReceipts">
            <slot name="receipt" :payment="payment">
              <button
                aria-label="download receipt"
                @click="$emit('buildReceipt', payment)"
              >
                <icon name="download" :display="{ size: 'b' }" />
              </button>
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
    <button
      v-if="offset < payments.length"
      class="c-button c-button--s has-bg-white has-box-shadow"
      type="button"
      @click="loadMore"
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

    interval: {
      type: Number,
      default: 7,
    },

    showReceipts: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return { offset: this.interval };
  },

  computed: {
    slicedPayments() {
      return this.payments.slice(0, this.offset);
    },
  },

  methods: {
    loadMore() {
      this.offset += this.interval;
    },
  },
};
</script>
