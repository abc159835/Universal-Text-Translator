<template>
    <div id="setting_background">
        <el-scrollbar class="box-card">
            <el-card style="width: 757px;">
                <template #header>
                    <div class="card-header">
                        <span style="font-size: larger;">全局设置</span>
                        <el-button class="button" type="success" @click="save">Save</el-button>
                    </div>
                </template>
                <el-form label-width="160px" label-position="right" >
                    <el-form-item label="提取规则">
                        <el-select v-model="rule" placeholder="Select">
                            <el-option v-for="item in rule_list" :key="item" :label="item" :value="item" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="翻译源">
                        <el-select v-model="translator" placeholder="Select">
                            <el-option v-for="item in translator_list" :key="item" :label="item" :value="item" />
                        </el-select>
                    </el-form-item>
                </el-form>
                <el-card>
                    <template #header>
                        <div class="card-header">
                            <span>翻译设置</span>
                        </div>
                    </template>
                    <Config :label-width="120" :config="translator_config"></Config>
                </el-card>
            </el-card>
        </el-scrollbar>
    </div>
</template>

<script setup lang="ts">
import { func_with_pywebview } from '~/func';
import { onActivated, ref, watch, getCurrentInstance } from 'vue';
import { ElSelect,ElMessage } from 'element-plus';
import Config from '~/components/Config.vue';

declare const pywebview: any

var rule_list = ref([])
var translator_list = ref([])
var config = ref({})
var translator_config = ref({})

var rule = ref('')
var translator = ref('')

const updata = () => {
    func_with_pywebview(async () => {
        rule.value = await pywebview.api._global_config("rule")        
        translator.value = await pywebview.api._global_config('translator')
        
        rule_list.value = await pywebview.api._get_variable("rule_list")
        translator_list.value = await pywebview.api._get_variable("translator_list")
        config.value = await pywebview.api._global_config(null)
        translator_config.value = await pywebview.api._get_translator_config(translator.value)
    })
}

const instance = getCurrentInstance()
if (instance) {
    const bus = instance.appContext.config.globalProperties.$bus
    bus.on('SettingUpdata',updata)
}

onActivated(() => {
    updata()
})

watch(translator,async () => {
    if(translator.value != '')
        translator_config.value = await pywebview.api._get_translator_config(translator.value)
})

const save = () => {
    func_with_pywebview(async () => {
        await pywebview.api._set_global_config('translator',translator.value)
        await pywebview.api._set_global_config('rule',rule.value)
        await pywebview.api._set_translator_config(translator.value,translator_config.value)
        ElMessage({
            showClose: true,
            message: '保存成功！',
            type: 'success',
            duration: 1000,
        })
    })
}
</script>


<style>
#setting_background {
    position: absolute;
    top: 40px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    background-color: aquamarine;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.box-card {
    width: 800px;
    height: 90%;
    margin: 4px;
}
</style>