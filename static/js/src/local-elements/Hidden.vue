<template>
  <input
    :value="value"
    :name="name"
    type="hidden"
  >
</template>

<script>
export default {
  name: 'Hidden',

  props: {
    value: {
      type: String,
      required: true,
    },

    name: {
      type: String,
      required: true,
    },
  },
};
</script>
