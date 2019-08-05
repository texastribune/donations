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
      return {
        url: {
          value: this.user.ambassador_url,
          rules: { url: true, required: true },
          shouldValidate: true,
          isVisible: true,
        },
      };
    },
  },

  methods: {
    async copyUrl(url) {
      try {
        await this.$copyText(url);
        this.didCopy = true;
      } catch (err) {
        // do nothing; just prevent
        // error page from appearing
      }
    },
  },
};
</script>
