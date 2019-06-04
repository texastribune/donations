<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-xxl-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg">
      <section class="c-detail-box">
        <div class="has-xxl-btm-marg"><info-list :items="data" /></div>

        <ul class="c-link-list t-linkstyle--underlined">
          <li>
            <span class="c-link-list__arrow has-text-teal">
              <strong>&rarr;</strong>
            </span>
            <router-link :to="{ name: 'blast-payments' }"
              >See your payment history</router-link
            >
          </li>
        </ul>
      </section>
    </div>

    <appeal />

    <help blast />
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
        { id: 0, heading: 'Subscription', text: '$329, yearly' },
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
