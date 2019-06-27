<template>
  <section class="c-detail-box">
    <div class="has-xxxl-btm-marg">
      <payment-list
        :payments="data"
        show-receipts
        @buildReceipt="buildReceipt"
      />
    </div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li v-if="isCancelled" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            href="/blastform"
            ga-on="click"
            :ga-event-category="ga.blastIntent.category"
            :ga-event-action="ga.blastIntent.actions['renew-blast']"
            :ga-event-label="ga.blastIntent.labels['user-portal']"
          >
            Renew your subscription to The Blast
          </a>
        </span>
      </li>
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link
            ga-on="click"
            :to="{ name: 'blast' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.inline"
            :ga-event-label="ga.userPortalNav.labels.blast"
          >
            More about your subscription
          </router-link>
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

    isCancelled: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    async buildReceipt({ date, amount, method }) {
      try {
        const buildBlastReceipt = await import(/* webpackChunkName: 'build-blast-receipt' */ '../build-blast-receipt');
        await buildBlastReceipt.default({
          date,
          amount,
          method,
        });
      } finally {
        window.dataLayer.push({
          event: this.ga.customEventName,
          gaCategory: this.ga.userPortal.category,
          gaAction: this.ga.userPortal.actions['blast-receipt'],
          gaLabel: this.ga.userPortal.labels['blast-payments'],
        });
      }
    },
  },
};
</script>
