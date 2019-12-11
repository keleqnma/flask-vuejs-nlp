import Vue from 'vue';
import Router from 'vue-router';
import Books from './components/Books.vue';

import Ping from './components/Ping.vue';
import BookDetail from './components/BookDetail.vue';
import ChapterDetail from './components/ChapterDetail.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [{
      path: '/',
      name: 'Books',
      component: Books,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/book',
      name: 'BookDetail',
      component: BookDetail,
    },
    {
      path: '/chapters',
      name: 'ChapterDetail',
      component: ChapterDetail,
    }
  ],
});
