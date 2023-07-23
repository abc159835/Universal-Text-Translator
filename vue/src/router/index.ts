// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Main from '../view/Main.vue'
import Setting from '../view/Setting.vue'
import TaskList from '../view/TaskList.vue'

const routes = [
  {
    path: '/',
    component: Main
  },
  {
    path: '/setting',
    component: Setting
  },
  {
    path: '/tasklist',
    component: TaskList
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router