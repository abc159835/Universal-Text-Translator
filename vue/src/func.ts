declare const pywebview:any

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

export const global_config = async (name:string,func:Function) => {
    var res = await pywebview.api.global_config(name)
    func(res)
}

export const set_global_config = debounce((name:string,value:any) => {
    pywebview.api.set_global_config(name,value)
},1000)