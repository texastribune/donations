<template>
  <div>
    <p class="has-xxxs-btm-marg has-text-gray-dark t-size-s t-space-heading-m">
      Or, copy your personal referral link:
    </p>
    <text-input-and-button
      :initial-fields="initialFields"
      :submit-text="submitText"
      read-only
      name="url"
      label="personal referral link"
      @onSubmit="copyUrl"
    />
  </div>
</template>

<script>
import TextInputAndButton from '../../../components/TextInputAndButton.vue';

export default {
  name: 'ReferralForm',

  components: { TextInputAndButton },

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
