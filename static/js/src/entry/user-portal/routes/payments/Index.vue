<template>
  <div class="has-white-bg has-ump-top-padding">
    <h1 class="has-xxl-btm-marg has-ump-side-padding">Your Donations</h1>

    <div class="has-ump-side-padding has-xl-btm-marg">
      <section class="c-detail-box">
        <div class="has-xxl-btm-marg">
          <payment-list :payments="payments" />
        </div>

        <ul class="c-link-list t-linkstyle--underlined">
          <li class="has-xs-btm-marg">
            <span class="c-link-list__arrow has-text-teal">
              <strong>&rarr;</strong>
            </span>
            <router-link :to="{ name: 'membership' }"
              >See your membership status</router-link
            >
          </li>
          <li class="has-xs-btm-marg">
            <span class="c-link-list__arrow has-text-teal">
              <strong>&rarr;</strong>
            </span>
            <a href="">Download your 2018 tax receipt</a>
          </li>
          <li>
            <span class="c-link-list__arrow has-text-teal">
              <strong>&rarr;</strong>
            </span>
            <a href="/donate#join-today">Become a sustaining member</a>
          </li>
        </ul>
      </section>
    </div>

    <appeal />

    <help membership />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';
import PaymentList from '../../components/PaymentList.vue';
import Appeal from '../../components/Appeal.vue';
import Help from '../../components/Help.vue';

export default {
  name: 'Index',

  components: { Appeal, PaymentList, Help },

  mixins: [routeMixin, routeFetchMixin],

  data() {
    return {
      payments: [
        { id: 0, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 1, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 2, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 3, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 4, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
      ],
    };
  },

  methods: {
    async fetchData() {
      return null;
    },
  },
};
</script>
