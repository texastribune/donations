<template>
  <div>
    <p class="has-xxxs-btm-marg has-text-gray-dark t-size-s">
      Or, share your personal referral link:
    </p>
    <text-input-and-submit
      name="url"
      label="Personal referral link"
      rules="required"
      read-only
      :submit-text="submitText"
      :initial-fields="initialFields"
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
    copyUrl(fields) {
      const url = fields.url.value;

      this.$emit('copyUrl', url);
    },
  },
};
</script>
