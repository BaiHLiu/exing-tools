import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import CovidTest from '@/components/CovidTest'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/hello',
            name: 'HelloWorld',
            component: HelloWorld
        },
        {
            path: '/covid_test',
            name: '核酸表格整理',
            component: CovidTest
        },
    ],
})


