<template>
<!-- 页面菜单栏 -->
<l-app-menu>
  <el-menu mode="horizontal" default-active="1" router :ellipsis="false" style="height: 100%;">
    <el-menu-item index="1" route="/">
      工作区
    </el-menu-item>
    <el-menu-item index="2" route="/tasklist">
      任务列表
    </el-menu-item>
    <el-menu-item index="3" route="/setting">
      设置
    </el-menu-item>
  </el-menu>
</l-app-menu>
<!-- 保证页面切换不会使状态丢失 -->
<router-view v-slot="{ Component }">
  <keep-alive>
    <component :is="Component" />
  </keep-alive>
</router-view>
</template>

<script lang="ts" setup>
import { func_with_pywebview, put_message } from './func'

declare const pywebview: any

func_with_pywebview(async () => {
  while (true) {
    const Message = await pywebview.api._get_message()
    put_message(Message)
    // if (Message.message.search('Detect') != -1)
    //   bus.emit('SettingUpdata')
  }
})
</script>

<style>
l-app-menu {
  position: absolute;
  top: 0px;
  height: 40px;
}

</style>