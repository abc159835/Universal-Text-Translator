<template>
    <div style="display: flex;align-items: center; height: 100%; margin-left:0px;">
        <el-button type="primary" :icon="Folder" @click="open_folder">Open Folder</el-button>
        <el-button type="primary" :icon="Folder" @click="export_folder">Export Folder</el-button>
        <el-tooltip v-if="rawcontent != ''" :content="rawcontent" raw-content>
            <el-button type="primary" :icon="InfoFilled" />
        </el-tooltip>
        <el-button type="success" @click="emit('menu_click','this')">Pre Translation</el-button>
        <el-tag v-if="file_path.length > 0" class="ml-3" size="large" style="font-size: small" effect="plain" type="success">{{ file_path }}</el-tag>
    </div>
</template>

<script setup lang="ts">
import { InfoFilled,Folder } from '@element-plus/icons-vue'
import { ElLoading } from 'element-plus'
import { watch } from 'vue'
import { set_global_config,func_with_pywebview,global_config } from '~/func'

declare const pywebview:any

var rawcontent = ''

var p = defineProps<{
    info: {}
    file_path: string
}>()

watch(p, () => {
    rawcontent = ''
    // 遍历属性名和值
    for (let [key, value] of Object.entries (p.info)) {
        rawcontent += key + ': ' + value + '<br>'
    }
})

// 事件声明
var emit = defineEmits<{
    (event: 'folder_change', data: []): void
    (event: 'menu_click', button: string): void
}>()

const open_folder = async () => {
    var path = await pywebview.api._open_folder()
    read_folder(path)
}

const export_folder = async () => {
    var path = await pywebview.api._open_folder()
    if (path)
        pywebview.api._create_export_task(path)
}

const read_folder = async (path: string) => {
    if (path) {
        const loading = ElLoading.service({
            lock: true,
            text: 'Loading',
            background: 'rgba(0, 0, 0, 0.7)',
        })
        var data = await pywebview.api._recursive_read_folder(path)
        if (data) {
            emit('folder_change', data)
            global_config('path',(res: string) => {
                if (res != path)
                    set_global_config('path', path)
            })
        }
        loading.close()
    }
}


func_with_pywebview(async () => {
    global_config('path', read_folder)
})

</script>