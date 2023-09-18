<template>
    <el-scrollbar height="100%">
        <el-card style="border-radius: 0px">
            <el-input v-model="filterText" placeholder="Filter keyword" />
            <el-tree highlight-current ref="treeRef" class="filter-tree" :data="data" :props="defaultProps" :filter-node-method="filterNode"
                @node-click="handleNodeClick" />
        </el-card>
    </el-scrollbar>
</template>
  
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ElMessage, ElTree } from 'element-plus'
import { TreeNodeData } from 'element-plus/es/components/tree/src/tree.type'
import { load_file } from '~/func'


declare const pywebview: any

interface Tree {
    label: string
    path: string
    children?: Tree[]
}

//文件数据
const p = defineProps<{
    data: Tree[]
    raw: Boolean
    modelValue: string
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
    (event: 'file_change', data: any, info: any, selection: any, lines: string[],bools :boolean[]): void
    (event: 'update:modelValue', res: string): void
}>()

const handleNodeClick = async (data: Tree) => {
    // 通过判断 是否具备children属性来判断 点击的是否是文件
    if (!Reflect.has(data, 'children')) {
        var datas = await load_file(data.path, p.raw)
        if (datas) {
            emit('file_change', datas.content, datas.info, datas.selection, datas.lines, datas.bools)
            emit('update:modelValue',data.path)
        }
        else {
            ElMessage.error(data.label + ' 不是一个有效的文本文件！')
        }   
    }
}

</script>
  