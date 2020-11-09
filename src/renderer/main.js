import Vue from 'vue'
import axios from 'axios'
import { Table, TableColumn, Popover, Tag, Button, Progress, Input, Divider } from 'element-ui'
import App from './App'
import router from './router'
import store from './store'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.component(Table.name, Table)
Vue.component(TableColumn.name, TableColumn)
Vue.component(Popover.name, Popover)
Vue.component(Tag.name, Tag)
Vue.component(Button.name, Button)
Vue.component(Progress.name, Progress)
Vue.component(Input.name, Input)
Vue.component(Divider.name, Divider)
/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
