<template>
  <input
    :value="value"
    :name="name"
    type="hidden"
  >
</template>

<script>
export default {
  name: 'LocalHidden',

  props: {
    name: {
      type: String,
      required: true,
    },

    value: {
      type: String,
      required: true,
    },
  },
};
</script>
