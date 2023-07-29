from threading import Thread
import traceback
import webview.util
import json

logger = webview.util.logger

def Error():
    from module.OShelper import put_message
    print(traceback.format_exc())
    put_message('error',traceback.format_exc(limit = 0),True)


def js_bridge_call(window, func_name, param, value_id):
    def _call():
        try:
            result = func(*func_params.values())
            result = json.dumps(result).replace('\\', '\\\\').replace('\'', '\\\'')
            code = 'window.pywebview._returnValues["{0}"]["{1}"] = {{value: \'{2}\'}}'.format(func_name, value_id, result)
        except Exception as e:
            Error()
            error = {
                'message': str(e),
                'name': type(e).__name__,
                'stack': traceback.format_exc()
            }
            # result = json.dumps(error).replace('\\', '\\\\').replace('\'', '\\\'')
            # code = 'window.pywebview._returnValues["{0}"]["{1}"] = {{isError: true, value: \'{2}\'}}'.format(func_name, value_id, result)
            result = json.dumps(None)
            code = 'window.pywebview._returnValues["{0}"]["{1}"] = {{value: \'{2}\'}}'.format(func_name, value_id, result)

        window.evaluate_js(code)

    if func_name == 'moveWindow':
        window.move(*param)
        return

    if func_name == 'asyncCallback':
        value = json.loads(param) if param is not None else None

        if callable(window._callbacks[value_id]):
            window._callbacks[value_id](value)
        else:
            logger.error('Async function executed and callback is not callable. Returned value {0}'.format(value))

        del window._callbacks[value_id]
        return

    func = window._functions.get(func_name) or getattr(window._js_api, func_name, None)

    if func is not None:
        try:
            func_params = param
            t = Thread(target=_call)
            t.start()
        except Exception:
            logger.exception('Error occurred while evaluating function {0}'.format(func_name))
    else:
        logger.error('Function {}() does not exist'.format(func_name))

webview.util.js_bridge_call = js_bridge_call