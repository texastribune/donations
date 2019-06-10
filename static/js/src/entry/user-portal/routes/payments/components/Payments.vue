<template>
  <section class="c-detail-box">
    <div class="has-xxxl-btm-marg"><payment-list :payments="data" /></div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <a href="#">Download your 2018 tax receipt</a>
      </li>
      <li v-if="isExpired && !isOneTime" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <a href="#">Renew your membership</a>
      </li>
      <li v-if="isOneTime" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <a href="#">Become a sustaining member</a>
      </li>
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <router-link :to="{ name: 'membership' }"
          >See your membership status</router-link
        >
      </li>
    </ul>
  </section>
</template>

<script>
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
};
</script>
