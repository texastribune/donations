<template>
  <text-input-and-button
    :rules="{ url: true, required: true }"
    :initial-fields="initialFields"
    :read-only="true"
    :submit-text="submitText"
    name="url"
    label="personal referral link"
    @onSubmit="copyUrl"
  />
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
    },
  },
};
</script>
