<template>
    <el-scrollbar height="100%">
        <el-input v-model="filterText" placeholder="Filter keyword" />
        <el-tree ref="treeRef" class="filter-tree" :data="data" :props="defaultProps" :filter-node-method="filterNode"
            @node-click="handleNodeClick" />
    </el-scrollbar>
</template>
  
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ElLoading, ElMessage, ElNotification, ElTree } from 'element-plus'
import { TreeNodeData } from 'element-plus/es/components/tree/src/tree.type'

declare const pywebview: any

interface Tree {
    label: string
    path?: string
    children?: Tree[]
}

//文件数据
defineProps<{
    data: Tree[]
}>()

const filterText = ref('')
const treeRef = ref<InstanceType<typeof ElTree>>()

const defaultProps = {
    children: 'children',
    label: 'label',
}

watch(filterText, (val) => {
    treeRef.value!.filter(val)
})

const filterNode = (value: string, data: TreeNodeData) => {
    if (!value) return true
    return data.label.includes(value)
}

// 事件声明
var emit = defineEmits<{
    (event: 'content_change', data: string, info:string): void
}>()

const handleNodeClick = async (data: Tree) => {
    if (!Reflect.has(data,'children')) {
        const loading = ElLoading.service({
            lock: true,
            text: 'Loading',
            background: 'rgba(0, 0, 0, 0.7)',
        })
        var datas = await pywebview.api.get_file_content(data.path)
        if (datas){
            var info = datas.info
            emit('content_change', datas.content,info)
        }
        else{
            ElMessage.error(data.label+' 不是一个有效的文本文件！')
        }
        loading.close()
    }
}

</script>
  