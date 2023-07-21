<template>
    <!-- <el-menu mode="horizontal" style="height: 100%;">
        <el-menu-item index="1" @click="open_folder">Open Folder</el-menu-item>
        <el-menu-item index="2">
            <el-button type="primary" :icon="Search">Search</el-button>
        </el-menu-item>
        <el-menu-item index="3">
            <el-tooltip :content="info" raw-content>
                <el-button type="primary" :icon="InfoFilled" />
            </el-tooltip>
        </el-menu-item>
    </el-menu> -->
    <div style="display: flex;align-items: center; height: 100%; margin-left: 8px;">
        <el-button type="primary" :icon="Folder" @click="open_folder">Open Folder</el-button>
        <el-button type="primary" :icon="Folder">Export Folder</el-button>
        <el-button type="primary" :icon="Folder">Setting</el-button>
        <el-button type="primary" :icon="Folder">Task List</el-button>
        <el-tooltip :content="info" raw-content>
            <el-button type="primary" :icon="InfoFilled" />
        </el-tooltip>
        <el-button type="success" >Auto Translation</el-button>
    </div>
</template>

<script setup lang="ts">
import { Search, InfoFilled,Folder } from '@element-plus/icons-vue'
import { ElLoading } from 'element-plus'
declare const pywebview:any

defineProps<{
    info: string
}>()

// 事件声明
var emit = defineEmits<{
    (event: 'project_change', data: Array<any>): void
}>()

const open_folder = async () => {
    var path = await pywebview.api.open_folder()
    if (path) {
        const loading = ElLoading.service({
            lock: true,
            text: 'Loading',
            background: 'rgba(0, 0, 0, 0.7)',
        })
        var data = await pywebview.api.recursive_read_folder(path)
        emit('project_change', data)
        loading.close()
    }
}


</script>