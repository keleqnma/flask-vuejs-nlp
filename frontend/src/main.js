import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './common/theme/index.css'
import './common/theme/github_corner.css'
import ElementUI from 'element-ui'

Vue.use(ElementUI);

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
