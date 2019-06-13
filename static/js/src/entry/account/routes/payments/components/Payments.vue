<template>
  <section class="c-detail-box">
    <div class="has-xxxl-btm-marg"><payment-list :payments="data" /></div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a href="#">Download your {{ lastYear }} tax receipt</a>
        </span>
      </li>
      <li v-if="isExpired && !isOneTime" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a href="#">Renew your membership</a>
        </span>
      </li>
      <li v-if="isOneTime" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a href="#">Become a sustaining member</a>
        </span>
      </li>
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link :to="{ name: 'membership' }"
            >See your membership status</router-link
          >
        </span>
      </li>
    </ul>
  </section>
</template>

<script>
import getYear from 'date-fns/get_year';

import PaymentList from '../../../components/PaymentList.vue';

export default {
  name: 'Payments',

  components: { PaymentList },

  props: {
    data: {
      type: Array,
      required: true,
    },

    isExpired: {
      type: Boolean,
      required: true,
    },

    isOneTime: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },
};
</script>
