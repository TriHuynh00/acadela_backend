from acadela.sacm.case_object.http_hook import HttpTrigger

def interpret_case_hook(hookObj):
    return {
        "event": hookObj.event,
        "url": hookObj.url
    }

def interpret_http_hook(httpHookObj):
    return HttpTrigger(httpHookObj.event,
                       httpHookObj.url,
                       httpHookObj.method,
                       httpHookObj.failureMessage)
