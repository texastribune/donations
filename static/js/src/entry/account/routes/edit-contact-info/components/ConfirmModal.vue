<template>
  <modal name="modal" width="80%" height="auto" :max-width="450" adaptive>
    <div class="c-modal">
      <div class="c-modal__top l-align-center-children has-padding">
        <h2 class="t-size-b t-align-center t-space-base">
          You have unsaved changes
        </h2>
      </div>
      <ul class="c-modal__buttons l-width-full">
        <li>
          <base-button
            text="Go back"
            :display="{ size: 's' }"
            @onClick="$emit('onReturn')"
          />
        </li>
        <li>
          <base-button
            text="Abandon changes"
            :display="{ size: 's' }"
            @onClick="$emit('onLeave')"
          />
        </li>
      </ul>
    </div>
    <button
      class="c-modal__close has-bg-white has-text-gray"
      aria-label="close modal"
      @click="$emit('onReturn')"
    >
      <icon name="close" :display="{ size: 'xxs', color: 'gray' }" />
    </button>
  </modal>
</template>

<script>
export default {
  name: 'EditContactInfoModal',
};
</script>
