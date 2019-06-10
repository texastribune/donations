<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      Your Donations
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box">
        <div class="has-xxxl-btm-marg">
          <payment-list :payments="payments" />
        </div>

        <ul class="c-link-list t-linkstyle--underlined">
          <li class="has-m-btm-marg">
            <span class="c-link-list__arrow has-text-teal">
              <strong>&rarr;</strong>
            </span>
            <router-link :to="{ name: 'membership' }"
              >See your membership status</router-link
            >
          </li>
          <li class="has-m-btm-marg">
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
import PaymentList from '../../components/PaymentList.vue';
import Appeal from '../home/containers/AppealContainer.vue';
import Help from '../../components/Help.vue';

export default {
  name: 'PaymentsRoute',

  components: { Appeal, PaymentList, Help },

  mixins: [routeMixin],

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
