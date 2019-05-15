<template>
  <div class="c-top-route">
    <h1 class="has-xxl-btm-marg">Your Membership</h1>

    <section class="has-xxl-btm-marg">
      <div class="has-xxl-btm-marg"><info-list :items="data" /></div>

      <ul class="c-link-list t-linkstyle--underlined">
        <li class="has-xs-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <router-link :to="{ name: 'payments' }"
            >See your donation history</router-link
          >
        </li>
      </ul>
    </section>

    <help membership />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';
import Help from '../../components/Help.vue';
import InfoList from '../../components/InfoList.vue';

export default {
  name: 'Index',

  components: { Help, InfoList },

  mixins: [routeMixin, routeFetchMixin],

  data() {
    return {
      data: [
        { id: 0, heading: 'Donation', text: '$35, monthly' },
        { id: 1, heading: 'Payment method', text: 'VISA ending in 4242' },
        { id: 2, heading: 'Next payment', text: 'March 29, 2019' },
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
