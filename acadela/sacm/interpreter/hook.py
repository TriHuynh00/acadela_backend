from acadela.sacm.case_object.http_hook import HttpTrigger

def interpret_case_hook(hookObj):
    return {
        "event": hookObj.event,
        "url": hookObj.url
    }

def interpret_http_hook(httpHookObj):
    return HttpTrigger(str.upper(httpHookObj.event),
                       httpHookObj.url,
                       str.upper(httpHookObj.method),
                       httpHookObj.failureMessage)
