<template>
  <div>
    <p class="has-xxxs-btm-marg has-text-gray-dark t-size-s">
      Or, share your personal referral link:
    </p>
    <text-input-and-submit
      :initial-fields="initialFields"
      :submit-text="submitText"
      read-only
      @onSubmit="copyUrl"
    />
  </div>
</template>

<script>
import TextInputAndSubmit from '../../../form/components/TextInputAndSubmit.vue';

export default {
  name: 'ReferralForm',

  components: { TextInputAndSubmit },

  props: {
    initialFields: {
      type: Object,
      required: true,
    },

    didCopy: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    submitText() {
      return this.didCopy ? 'Copied!' : 'Copy';
    },
  },

  methods: {
    copyUrl({ url: { value } }) {
      this.$emit('copyUrl', value);

      window.dataLayer.push({
        event: this.ga.ambassadorsCustomEventName,
        gaCategory: this.ga.tribuneAmbassadors.category,
        gaAction: this.ga.tribuneAmbassadors.actions.link,
        gaLabel: this.ga.tribuneAmbassadors.labels.ambassador,
      });
    },
  },
};
</script>
