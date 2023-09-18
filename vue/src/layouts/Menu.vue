<template>
    <div style="display: flex;align-items: center; height: 100%; margin-left:0px;">
        <el-button type="primary" :icon="Folder" @click="open_folder">Open Folder</el-button>
        <el-button type="primary" :icon="Folder" @click="export_folder">Export Folder</el-button>
        <el-tooltip v-if="rawcontent != ''" :content="rawcontent" raw-content>
            <el-button type="primary" :icon="InfoFilled" />
        </el-tooltip>
        <el-button v-if="raw" type="success" style="width: 120px;" @click="emit('savefile')">Save File</el-button>
        <el-button v-else type="success" style="width: 120px;" @click="dialogFormVisible = true">Pre Translation</el-button>
        <el-dialog v-model="dialogFormVisible" title="创建任务">
            <el-form label-position="right" label-width="240px">
                <el-form-item label="翻译文件选择:">
                    <el-select v-model="file_select">
                        <el-option label="当前文件" value="this" />
                        <el-option label="所有文件" value="all" />
                    </el-select>
                </el-form-item>
                <el-form-item label="其它:">
                    <el-checkbox v-model="trans_history">启用翻译历史</el-checkbox>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="dialogFormVisible = false; emit('menu_click',{file: file_select,history: trans_history})">
                        Confirm
                    </el-button>
                </span>
            </template>
        </el-dialog>
        <el-tag v-if="file_path.length > 0" class="ml-3" size="large" style="font-size: small" effect="plain"
            type="success">{{ file_path }}</el-tag>
    </div>
</template>

<script setup lang="ts">
import { InfoFilled, Folder } from '@element-plus/icons-vue'
import { ElLoading } from 'element-plus'
import { watch, ref } from 'vue'
import { set_global_config, func_with_pywebview, global_config } from '~/func'

declare const pywebview: any

var rawcontent = ''
const dialogFormVisible = ref(false)
const file_select = ref('this')
const trans_history = ref(true)

var p = defineProps<{
    info: {}
    file_path: string
    raw: boolean
}>()

watch(p, () => {
    rawcontent = ''
    // 遍历属性名和值
    for (let [key, value] of Object.entries(p.info)) {
        rawcontent += key + ': ' + value + '<br>'
    }
})

// 事件声明
var emit = defineEmits<{
    (event: 'folder_change', data: []): void
    (event: 'menu_click', button: {}): void
    (event: 'savefile'): void
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
            global_config('path', (res: string) => {
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