<template>
  <section class="c-detail-box">
    <div class="has-xxxl-btm-marg"><payment-list :payments="data" /></div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link :to="{ name: 'blast' }"
            >More about your subscription</router-link
          >
        </span>
      </li>
    </ul>
  </section>
</template>

<script>
import PaymentList from '../../../components/PaymentList.vue';

export default {
  name: 'BlastPayments',

  components: { PaymentList },

  props: {
    data: {
      type: Array,
      required: true,
    },
  },
};
</script>
