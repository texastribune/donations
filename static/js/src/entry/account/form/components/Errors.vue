<template>
  <ul>
    <li
      v-for="(message, index) in errorMessages"
      :key="message"
      :class="{ 'has-xs-btm-marg': index !== errorMessages.length - 1 }"
      class="has-text-error t-size-xs"
    >
      {{ message }}
    </li>
  </ul>
</template>

<script>
export default {
  name: 'FormElementErrors',

  props: {
    errorMessages: {
      type: Array,
      required: true,
    },
  },
};
</script>
