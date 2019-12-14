<template>
  <div id="app">
    <div
      style="text-align: right; font-size: 15px;  background-color: #b3c0d1;
        color: #333;
        line-height: 60px; font-family: Helvetica"
    >COCO LITERATURE</div>
    <router-view />
  </div>
</template>
<script>
export default {
  data() {
    return {
      routerAlive: true
    };
  },
  provide() {
    //在父组件中创建属性
    return {
      routerRefresh: this.routerRefresh
    };
  },
  methods: {
    routerRefresh() {
      this.routerAlive = false;
      this.$nextTick(() => {
        this.routerAlive = true;
      });
    }
  }
};
</script>
<style>
#app {
}
</style>
