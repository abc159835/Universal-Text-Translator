<template>
    <div style="display: flex;align-items: center; height: 100%; margin-left:0px;">
        <el-button type="primary" :icon="Folder" @click="open_folder">Open Folder</el-button>
        <el-button type="primary" :icon="Folder">Export Folder</el-button>
        <el-tooltip :content="infos" raw-content>
            <el-button type="primary" :icon="InfoFilled" />
        </el-tooltip>
        <el-button type="success" >Auto Translation</el-button>
    </div>
</template>

<script setup lang="ts">
import { InfoFilled,Folder } from '@element-plus/icons-vue'
import { ElLoading } from 'element-plus'
import { watch } from 'vue'
declare const pywebview:any

var infos = ''

var p = defineProps<{
    info: string
}>()

watch(p, () => {
    infos = ''
    // 遍历属性名和值
    for (let [key, value] of Object.entries (p.info)) {
        infos += key + ': ' + value + ' '
    }
})

// 事件声明
var emit = defineEmits<{
    (event: 'project_change', data: Array<any>): void
}>()

const open_folder = async () => {
    var path = await pywebview.api._open_folder()
    if (path) {
        const loading = ElLoading.service({
            lock: true,
            text: 'Loading',
            background: 'rgba(0, 0, 0, 0.7)',
        })
        var data = await pywebview.api._recursive_read_folder(path)
        emit('project_change', data)
        loading.close()
    }
}


</script>