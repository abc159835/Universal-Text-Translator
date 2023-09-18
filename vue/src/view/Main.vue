<template>
  <r-app-menu>
    <Menu 
      :info="info" 
      :file_path="file_path" 
      :raw="raw"
      @folder_change="(data) => { file_data = data; init()}" 
      @menu_click="handle_menu_click"
      @savefile="raw_file_save"
    >
    </Menu>
  </r-app-menu>

  <l-navigation-drawer :style="slider_style">
    <TreeView 
      v-model="abs_file_path"
      :raw="raw" 
      :data="file_data" 
      @file_change="file_change">
    </TreeView>
    <Sash location="right" v-model="slider_width" />
  </l-navigation-drawer>

  <r-navigation-drawer :style="operate_style">
    <Opreate 
      v-if = "position > -1"
      @handle_click="handle_click" 
      :original_text="original_text" 
      :line_count="line_count" 
      :position="position + 1"
      :loading="translate_loading"
      :raw="raw"
      v-model="translated_text" 
    />
    <Sash location="left" v-model="operate_width" />
  </r-navigation-drawer>

  <main id="editorContainer" :style="main_style"></main>
</template>

<script lang="ts" setup>
import Sash from '../components/Sash.vue';
import Menu from '../layouts/Menu.vue'
import TreeView from '../layouts/TreeView.vue';
import Opreate from '../layouts/Opreate.vue';
import { ref, watch, computed, onMounted,Ref } from 'vue';
import { global_config, set_global_config, func_with_pywebview, reactive_with_watch, throttle, debounce, load_file, put_message } from '~/func'
import { initEditor, decorate_selections, to_selections } from '~/monaco_editor';
import * as monaco from 'monaco-editor'

declare const pywebview: any

// 初始宽度
const slider_width = ref(320)
const operate_width = ref(320)

func_with_pywebview(() => {
  // 读取配置
  global_config('slider_width', (res: number) => {
    slider_width.value = res
  })

  global_config('operate_width', (res: number) => {
    operate_width.value = res
  });
})

const main_style = reactive_with_watch({
  left: computed(() => slider_width.value + 'px'),
  right: computed(() => operate_width.value + 'px')
})

const slider_style = reactive_with_watch({
  width: computed(() => slider_width.value + 'px')
})

const operate_style = reactive_with_watch({
  width: computed(() => operate_width.value + 'px')
})

// 监视变化，更新相关属性。
watch(slider_width, () => set_global_config('slider_width', slider_width.value))
watch(operate_width, () => set_global_config('operate_width', operate_width.value))

// 全局
var editor: monaco.editor.IStandaloneCodeEditor

onMounted(() => {
  const editorContainer = document.getElementById('editorContainer')
  if (editorContainer) {
    // 创建Monaco_editor
    editor = initEditor(editorContainer)
  }
})

// 文件树信息
const file_data = ref([])
const info: Ref<any> = ref({})
const abs_file_path = ref('')
const file_path = ref('')
const original_text = ref('')
const translated_text = ref('')
const line_count = ref(0)
const translate_loading = ref(false)
const raw = ref(false)

var position = -1
var lines: string[] = []
var selections: Array<monaco.Selection> = []
var decorations: Array<{ range: any, options: any }> = []
var decorationsCollection: monaco.editor.IEditorDecorationsCollection

const init = () => {
  editor.setValue('')
  position = -1
  original_text.value = ''
  translated_text.value = ''
  file_path.value = ''
}

const file_change = (text: string, infomation: any, arrays: any, _lines: string[], bools: boolean[]) => {
  if (file_path.value != infomation.Path)
    init()

  // setValue 后才能 getModel
  editor.setValue(text)


  lines = _lines

  info.value = infomation
  file_path.value = infomation.Path
  line_count.value = arrays.length

  if (arrays.length > 0) {
    if (file_path.value != infomation.Path || position == -1)
      position = 0
    selections = to_selections(arrays)
    decorations = decorate_selections(selections, bools)
    decorationsCollection = editor.createDecorationsCollection(decorations)
    flash_Position()
  }
}

const flash_Position = throttle(() => {
  var now_posi = editor.getPosition()
  var posi = selections[position].getEndPosition()
  if (now_posi && now_posi.column > posi.column) {
    var posi = selections[position].getStartPosition()
  }

  var temp = decorations[position].options.inlineClassName
  decorations[position].options.inlineClassName = 'InlineDecorationHighlight'
  decorationsCollection.set(decorations)
  decorations[position].options.inlineClassName = temp

  editor.setPosition(posi)
  editor.revealPosition(posi)
  original_text.value = lines[position]
  get_translation()
},60)

const get_translation = debounce(async () => {
  translated_text.value = await pywebview.api._get_translation(original_text.value)
},200)

const edit_text = () => {
  if (translated_text.value && translated_text.value.length > 0 && position > -1) {
    var translated_text_value = translated_text.value.replaceAll('\n','\t')
    pywebview.api._updata_translation(original_text.value,translated_text_value)
    if (!raw.value) {
      editor.updateOptions({ readOnly: false })
      editor.executeEdits('user', [{ range: selections[position], text: translated_text_value }])
      var line_number = selections[position].startLineNumber
      var offset = translated_text_value.length - selections[position].endColumn + selections[position].startColumn
      selections[position] = selections[position].setEndPosition(line_number, selections[position].endColumn + offset)
      decorations[position].range = selections[position]
      decorations[position].options.inlineClassName = 'InlineDecorationHighlight'
      var temp = position
      if(selections.length > temp + 1) {
        temp++
        while(selections[temp].startLineNumber == line_number) {
          selections[temp] = new monaco.Selection(line_number,selections[temp].startColumn + offset,line_number,selections[temp].endColumn + offset)
          decorations[temp].range = selections[temp]
          if(selections.length > temp + 1)
            temp++
          else
            break
        }
      }
      decorationsCollection.set(decorations)
      decorations[position].options.inlineClassName = '_InlineDecoration'
      editor.updateOptions({ readOnly: true })
    }
    put_message({
      box: false,
      message: '提交成功！',
      level: 'success'
    })
  }
  else 
  put_message({
      box: false,
      message: '无法提交！',
      level: 'error'
    })
}

const handle_menu_click = (button: any) => {
  switch (button.file) {
    case 'this':
      if (position > -1) {
        pywebview.api._create_translate_task(file_path.value,lines,button.history)
        return
      }
      break
    case 'all':
      if (file_data.value.length > 0) {
        pywebview.api._create_translate_all_task(file_data.value,button.history)
        return
      }
      break
  }
  put_message({
    box: false,
    message: '无效操作',
    level: 'error'
  })
}

const raw_file_save = () => {
  if (abs_file_path.value.length > 0 && raw.value) {
    var model = editor.getModel()
    if (model)
      pywebview.api._save_file(abs_file_path.value,model.getValue(),info.value.Encoding)
    put_message({
      box: false,
      message: '已保存更改！',
      level: 'success'
    })
  }
}


const handle_click = async (button: any) => {
  // 当上一步报错时，解锁
  translate_loading.value = false
  var old_posi = position
  switch (button) {
    case 'change':
      raw.value = !raw.value
      editor.updateOptions({ readOnly: !raw.value })
      if (position > -1) {
        var datas = await load_file(abs_file_path.value,raw.value)
        if (datas)
          file_change(datas.content, datas.info, datas.selection, datas.lines, datas.bools)
      }
      break
    case 'translate':
      translate_loading.value = true
      var res = await pywebview.api._translate(original_text.value)
      if (position == old_posi)
        translated_text.value = res
      translate_loading.value = false
      break
    case 'back':
      position > 0 ? position -= 1 : position
      break
    case 'next':
      position < selections.length - 1 ? position += 1 : position
      break
    case 'submit':
      edit_text();
      break
    default:
      position = position == -1 ? -1 : button - 1
      break
  }
  if (old_posi != position) flash_Position()
}

</script>

<style>
.InlineDecoration {
  background-color: white;
}

._InlineDecoration {
  background-color: antiquewhite;
}

.InlineDecorationHighlight {
  background-color: gold;
}

r-app-menu {
  position: absolute;
  top: 0px;
  left: 320px;
  height: 40px;
}

main {
  position: absolute;
  top: 40px;
  bottom: 0px;
}

l-navigation-drawer {
  position: absolute;
  top: 40px;
  bottom: 0px;
  left: 0px;
  background-color: aquamarine;
}

r-navigation-drawer {
  position: absolute;
  top: 40px;
  bottom: 0px;
  right: 0px;
  background-color: antiquewhite;
}
</style>