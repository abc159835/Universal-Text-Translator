declare const pywebview: any

//防抖函数
export const debounce = (fn: Function, debTime: number) => {
    let timer: any = null;
    return (...args: any[]) => {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
            fn.apply(this, args);
            timer = null;
        }, debTime)
    }
}

// 节流函数，且最后一次也执行。
export const throttle = (fn: Function, rateTime: number) => {
    let timer: any = null;
    let prev = Date.now() - rateTime;
    return (...args: any[]) => {
        let remaining = rateTime - (Date.now() - prev);
        clearTimeout(timer);
        if (remaining <= 0) {
            fn.apply(this, args);
            prev = Date.now();
        } else {
            timer = setTimeout(() => {
                fn.apply(this, args)
            }, remaining)
        }
    }
}

export const global_config = async (name: string, func: Function) => {
    var res = await pywebview.api._global_config(name)
    func(res)
}

export const set_global_config = debounce((name: string, value: any) => {
    pywebview.api._set_global_config(name, value)
}, 100)

//安全的执行要调用api的方法
export const func_with_pywebview = (func: Function) => {
    if (typeof pywebview !== "undefined") {
        func()
    }
    else {
        // 监听 window.pywebviewready 事件
        window.addEventListener("pywebviewready", () => {
            func()
        })
    }
}

import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import { watch, reactive, isRef, Ref } from "vue"
export const reactive_with_watch = (object: { [key: string]: any | Ref<any> }) => {
    for (const [key, value] of Object.entries(object)) {
        if (isRef(value)) {
            object[key] = value.value // 同步ref的内部值
            watch(value, newValue => object[key] = newValue) // 监听ref的变化
        }
    }
    return reactive(object) // 返回响应式对象
}


func_with_pywebview(async () => {
    while (true) {
      const Message = await pywebview.api._get_message()
      put_message(Message)
    }
  })

export const put_message = (Message: any) => {
    if (Message.box)
        ElMessageBox.confirm(Message.message, 'SYSTEM', {
          confirmButtonText: 'Copy',
          type: Message.level,
        }).then(() => {
          pywebview.api._copy(Message.message)
        })
      else
        ElMessage({
          showClose: true,
          message: Message.message,
          type: Message.level
        })
}

export const load_file = async (path: string ,raw :Boolean) => {
    const loading = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
    })
    var datas = await pywebview.api._get_file_content(path,!raw)
    loading.close()
    return datas
  }