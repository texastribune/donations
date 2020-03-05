<template>
  <referral-form
    :initial-fields="initialFields"
    :did-copy="didCopy"
    @copyUrl="copyUrl"
  />
</template>

<script>
import userMixin from '../../../store/user/mixin';

import ReferralForm from '../components/ReferralForm.vue';

export default {
  name: 'ReferralFormContainer',

  components: { ReferralForm },

  mixins: [userMixin],

  data() {
    return { didCopy: false };
  },

  computed: {
    initialFields() {
      return { url: this.user.ambassadorUrl };
    },
  },

  methods: {
    async copyUrl(url) {
      try {
        await this.$copyText(url);

        this.didCopy = true;

        setTimeout(() => {
          this.didCopy = false;
        }, 1000);

        window.dataLayer.push({
          event: this.ga.ambassadorsCustomEventName,
          gaCategory: this.ga.tribuneAmbassadors.category,
          gaAction: this.ga.tribuneAmbassadors.actions.link,
          gaLabel: this.ga.tribuneAmbassadors.labels.ambassador,
        });
      } catch (err) {
        // do nothing; just prevent
        // error page from appearing
      }
    },
  },
};
</script>
