<template>
    <div id="tasklist_background">
        <el-scrollbar class="box-card">
            <el-card>
                <template #header>
                    <span>任务状态</span>
                </template>
                <el-card class="mb-3" v-if="tasks.length > 0" v-for="task in tasks">
                    <el-descriptions :column="1" >
                        <template #title>
                            <div class="container">
                                <el-tag size="large" style="font-size: medium;" type="success" effect="plain">{{ task.name }}</el-tag>
                                <el-button class="item" type="danger" circle :icon="Delete" @click="cancel_task(task.name)"></el-button>
                            </div>
                        </template>
                        <el-descriptions-item >
                            <template #label>
                                <el-tag style="font-size: medium;" type="info">进度</el-tag>
                            </template>
                            <el-tag style="font-size: medium;" type="info">
                                {{ task.progress }} / {{ task.end_progress }}
                            </el-tag>
                        </el-descriptions-item>
                        <el-descriptions-item label="Info" style="max-width: max-content;">
                            <template #label>
                                <el-tag style="font-size: medium;" type="info">状态</el-tag>
                            </template>
                            <el-tag style="font-size: medium;" type="info">
                                {{ showMore(task.info) }}
                            </el-tag>
                        </el-descriptions-item>
                        
                    </el-descriptions>
                    <el-progress :percentage="Number((task.progress * 100 / task.end_progress).toFixed(1))" :text-inside="true" :stroke-width="15"/>
                </el-card>
                <el-empty v-else description="没有正在进行的任务" />
            </el-card>
        </el-scrollbar>
    </div>
</template>

<script setup lang="ts">
import { onActivated, onDeactivated, ref } from 'vue';
import { func_with_pywebview } from '~/func';
import { Delete } from '@element-plus/icons-vue'

declare const pywebview: any
const tasks: any = ref([])

var timer: NodeJS.Timer

onActivated(() => {
    timer = setInterval(updata,200)
})

const showMore = (line: string) => {
    if (line.length > 38)
        line = line.substring(0,38) + '...'
    return line
}

const updata = () => {
    func_with_pywebview(async () => {
        tasks.value = await pywebview.api._get_all_tasks_status()
    })
}

const cancel_task = (uuid: string) => {
    func_with_pywebview(async () => {
        await pywebview.api._cancel_task(uuid)
    })
}

onDeactivated(() => {
    clearInterval(timer)
})

</script>

<style>
#tasklist_background {
    position: absolute;
    top: 40px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    background-color: antiquewhite;
    display: flex;
    align-items: center;
    justify-content: center;
}


.container {
  position: relative; /* 创建相对定位的容器 */
}


.item {
  position: absolute; /* 创建绝对定位的元素 */
  left: 680px;
  top: 45px
}

</style>