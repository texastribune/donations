<template>
  <input :value="value" :name="name" type="hidden" />
</template>

<script>
export default {
  name: 'Hidden',

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
