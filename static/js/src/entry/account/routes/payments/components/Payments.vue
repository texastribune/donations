<template>
  <section class="c-detail-box">
    <div class="has-b-btm-marg"><payment-list :payments="data" /></div>

    <p
      class="t-size-xs t-linkstyle--underlined t-space-heading-m has-text-gray has-xxxl-btm-marg"
    >
      Note: Donation history does not include event sponsorships or ticket
      purchases. To receive a {{ lastYear }} tax receipt with this information,
      please contact
      <a
        href="mailto:community@texastribune.org"
        ga-on="click"
        :ga-event-category="ga.userPortal.category"
        :ga-event-action="ga.userPortal.actions['contact-us']"
        :ga-event-label="ga.userPortal.labels.payments"
        >community@texastribune.org</a
      >.
    </p>

    <ul class="c-link-list t-linkstyle--underlined">
      <li v-if="totalGiftsLastYear > 0" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <button class="c-link-button" @click="buildReceipt">
            Download your {{ lastYear }} tax receipt
          </button>
        </span>
      </li>
      <li v-if="!isMDev && isExpired" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            :href="isFormerCircle ? circleUrl : donateUrl"
            ga-on="click"
            :ga-event-category="ga.donations.category"
            :ga-event-action="ga.donations.actions['membership-intent']"
            :ga-event-label="ga.donations.labels['renew-membership']"
          >
            Renew your membership
          </a>
        </span>
      </li>
      <li v-else-if="isOneTime && !isMDev" class="has-m-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            ga-on="click"
            :href="donateUrl"
            :ga-event-category="ga.donations.category"
            :ga-event-action="ga.donations.actions['membership-intent']"
            :ga-event-label="ga.donations.labels['upgrade-membership']"
          >
            Become a sustaining member
          </a>
        </span>
      </li>
      <li v-if="!isMDev">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link
            ga-on="click"
            :to="{ name: 'membership' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.inline"
            :ga-event-label="ga.userPortalNav.labels.membership"
          >
            See your membership status
          </router-link>
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
      validator: value => typeof value === 'boolean' || value === null,
      required: true,
    },

    isOneTime: {
      type: Boolean,
      required: true,
    },

    isFormerCircle: {
      type: Boolean,
      required: true,
    },

    isMDev: {
      type: Boolean,
      required: true,
    },

    greeting: {
      type: String,
      required: true,
    },

    totalGiftsLastYear: {
      type: Number,
      required: true,
    },
  },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },

  methods: {
    async buildReceipt() {
      try {
        const buildTaxReceipt = await import(/* webpackChunkName: 'build-tax-receipt' */ '../build-tax-receipt');
        const { lastYear, totalGiftsLastYear, greeting } = this;

        await buildTaxReceipt.default({
          lastYear,
          totalGiftsLastYear,
          greeting,
        });
      } finally {
        window.dataLayer.push({
          event: this.ga.customEventName,
          gaCategory: this.ga.userPortal.category,
          gaAction: this.ga.userPortal.actions['tax-receipt'],
          gaLabel: this.ga.userPortal.labels.payments,
        });
      }
    },
  },
};
</script>
