<template>
    <ul :class="classes">
      <li v-for="(option, index) in options" :key="option.id">
        <input
          :id="index"
          :value="option.value"
          :name="name"
          :checked="value === option.value"
          type="radio"
          @change="onChange"
        />
        <label>{{ option.text }}</label>
      </li>
    </ul>
</template>
  
<script>
  import formElementMixin from '../mixins/element';

  import Errors from './Errors.vue';
  
  export default {
    name: 'Frequency',
  
    components: { Errors },

    mixins: [formElementMixin],

    props: {
      options: {
        type: Array,
        required: true,
      },
    },
  
    methods: {
      onChange(event) {
        this.$emit('input', event.target.value);
      },
    },
  };
  </script>
  